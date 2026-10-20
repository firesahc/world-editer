"""Chunk 数据视图 —— 1.12 chunk NBT 的唯一数据形状适配层。

存在的理由
----------
1.12 的 NBT 值表示是**异构**的（顶层字段带 tag、list 元素不带 tag、
byte array 双层嵌套）。业务层如果各自判别形态，判别逻辑会散落多处并互相分叉
——历史上 `block.read_block` 就因为写错而恒返回空气。

职责边界
--------
* ``nbt.py``    —— NBT 二进制编解码 + 值表示的访问器
* ``region.py`` —— region 文件与扇区 IO（文件 ↔ chunk 字节）
* ``chunk.py``  —— **本模块**：chunk 字节 → 归一化的 tile / 方块视图
* ``tile.py`` / ``block.py`` —— 业务语义（按坐标查改 tile、id↔名字）

依赖方向单向：tile / block → chunk → region → nbt。
"""
from __future__ import annotations

from pathlib import Path

from . import nbt as nb


class Chunk:
    """一个已加载的 1.12 chunk 的读写视图。

    构造一次、多次查询，避免逐点重读 chunk（逐点 read_block 是 O(n²)）。

    写入路径依赖**保留 NBT 树**：`set_block` 改的是树里 `Sections[].Blocks/Data`
    的字节数组，`to_bytes` 再把树序列化回去。已实测
    `read_root → write_root` 字节无损，往返安全。
    """

    __slots__ = ("_name", "_root", "_tiles", "_sections",
                 "_blocks", "_data", "_sd", "_cx", "_cz")

    def __init__(self, nbt_bytes: bytes, cx=None, cz=None):
        name, comp, _ = nb.read_root(nbt_bytes)
        self._name = name
        self._root = comp
        self._cx = cx
        self._cz = cz
        lvl = nb.as_compound(comp)
        if lvl is None:
            lvl = {}
        else:
            lvl = nb.as_compound(lvl.get("Level")) or lvl

        self._tiles = self._parse_tiles(lvl)
        self._sections = nb.as_list(lvl.get("Sections")) or []
        # section Y -> (section compound, Blocks bytes, Data bytes)
        self._blocks = {}
        self._data = {}
        self._sd = {}
        for sec in self._sections:
            sd = nb.as_compound(sec)
            if sd is None:
                continue
            sy = nb.unwrap(sd.get("Y"))
            if not isinstance(sy, int):
                continue
            self._sd[sy] = sd
            b = nb.as_bytes(sd.get("Blocks"))
            d = nb.as_bytes(sd.get("Data"))
            if b:
                self._blocks[sy] = b
            if d:
                self._data[sy] = d

    # ---------------------------------------------------------------- tiles

    @staticmethod
    def _parse_tiles(lvl):
        items = nb.as_list(lvl.get("TileEntities")) or []
        out = []
        for it in items:
            d = nb.as_compound(it)
            if d is None:
                continue
            attrs = {k: nb.unwrap(v) for k, v in d.items()}
            out.append(attrs)
        return out

    def tiles(self):
        """本 chunk 内全部 TileEntity（字段已 unwrap）。"""
        return list(self._tiles)

    def tile_at(self, x, y, z):
        """按**块坐标**精确定位一个 TileEntity，找不到返回 None。"""
        for t in self._tiles:
            if t.get("x") == x and t.get("y") == y and t.get("z") == z:
                return t
        return None

    def tiles_of_id(self, tile_id):
        return [t for t in self._tiles if t.get("id") == tile_id]

    # ---------------------------------------------------------------- blocks

    @staticmethod
    def _index(x, y, z):
        return ((y & 15) << 8) | ((z & 15) << 4) | (x & 15)

    def block_at(self, x, y, z):
        """取 (block_id, meta)。空方块返回 (0, 0)。"""
        sy = y >> 4
        b = self._blocks.get(sy)
        if not b:
            return 0, 0
        si = self._index(x, y, z)
        if si >= len(b):
            return 0, 0
        bid = b[si]
        meta = 0
        d = self._data.get(sy)
        if d:
            idx = si >> 1
            if idx < len(d):
                meta = (d[idx] >> ((si & 1) << 2)) & 0x0F
        return bid, meta

    def block_name_at(self, x, y, z):
        from .block import block_name
        bid, meta = self.block_at(x, y, z)
        return bid, meta, block_name(bid)

    # ---------------------------------------------------------------- 写

    def set_block(self, x, y, z, block_id, meta=0):
        """设置一个地形方块，返回是否真的发生了变化。

        定位是**按坐标**的（只动一个确定的数组下标），因此不存在
        `tile_set` 那种"按字段名+旧值做字节匹配"的歧义问题 ——
        永远不会误伤同 chunk 里的其它方块或 tile。
        """
        sy = y >> 4
        sd = self._sd.get(sy)
        if sd is None:
            return False
        b = self._blocks.get(sy)
        if not b:
            return False
        si = self._index(x, y, z)
        if si >= len(b):
            return False
        meta &= 0x0F
        blocks = bytearray(b)
        data = bytearray(self._data.get(sy, b""))
        old_id = blocks[si]
        idx = si >> 1
        old_meta = 0
        if idx < len(data):
            old_meta = (data[idx] >> ((si & 1) << 2)) & 0x0F
        if old_id == block_id and old_meta == meta:
            return False
        blocks[si] = block_id
        if idx < len(data):
            shift = (si & 1) << 2
            data[idx] = (data[idx] & ~(0x0F << shift)) | (meta << shift)
        # 写回树里，保持 _blocks/_data 与树同步
        self._blocks[sy] = bytes(blocks)
        self._data[sy] = bytes(data)
        sd["Blocks"] = (nb.TAG_BYTE_ARRAY, ("bytearray", bytes(blocks)))
        if data:
            sd["Data"] = (nb.TAG_BYTE_ARRAY, ("bytearray", bytes(data)))
        return True

    def to_bytes(self):
        """把（可能已被修改的）树序列化回 chunk NBT 字节。"""
        return nb.write_root(self._name, self._root)

    # ---------------------------------------------------------------- 比对

    def diff(self, other):
        """与另一个 chunk 视图做**语义**比对。

        噪声字段（每次保存都会自然变化）被忽略：
          chunk 级 —— LastUpdate / HeightMap / LightPopulated / TileTicks
                      / TerrainPopulated / InhabitedTime
          tile  级 —— LastExecution / LastOutput

        返回 {"blocks": [...], "tiles": [...]}，坐标为世界坐标。
        """
        chunks = [
            "LastUpdate", "HeightMap", "LightPopulated", "TileTicks",
            "TerrainPopulated", "InhabitedTime",
        ]
        tile_noise = ["LastExecution", "LastOutput"]

        # --- 方块层：先比原始 bytes，相同则跳过逐位置扫描 ---
        block_diffs = []
        for sy in sorted(set(self._blocks) | set(other._blocks)):
            b1 = self._blocks.get(sy, b"")
            b2 = other._blocks.get(sy, b"")
            d1 = self._data.get(sy, b"")
            d2 = other._data.get(sy, b"")
            if b1 == b2 and d1 == d2:
                continue
            base_x = (self._cx if self._cx is not None else 0) * 16
            base_z = (self._cz if self._cz is not None else 0) * 16
            for y in range(sy * 16, sy * 16 + 16):
                for lz in range(16):
                    for lx in range(16):
                        si = self._index(lx, y, lz)
                        if si >= len(b1) or si >= len(b2):
                            continue
                        i1 = b1[si]
                        i2 = b2[si]
                        m1 = self._meta_at(d1, si)
                        m2 = self._meta_at(d2, si)
                        if i1 == i2 and m1 == m2:
                            continue
                        block_diffs.append({
                            "pos": [base_x + lx, y, base_z + lz],
                            "before": [i1, m1],
                            "after": [i2, m2],
                        })

        # --- tile 层：按坐标对齐比较字段 ---
        t1 = {(t.get("x"), t.get("y"), t.get("z")): t for t in self._tiles}
        t2 = {(t.get("x"), t.get("y"), t.get("z")): t for t in other._tiles}
        tile_diffs = []
        for coord in sorted(set(t1) | set(t2), key=lambda c: (str(c))):
            a = t1.get(coord, {})
            b = t2.get(coord, {})
            if a.get("id") != b.get("id"):
                tile_diffs.append({
                    "pos": list(coord), "field": "id",
                    "before": a.get("id"), "after": b.get("id"),
                })
            for k in sorted(set(a) | set(b)):
                if k in tile_noise or k in ("x", "y", "z"):
                    continue
                if a.get(k) != b.get(k):
                    tile_diffs.append({
                        "pos": list(coord), "field": k,
                        "before": a.get(k), "after": b.get(k),
                    })
        return {"blocks": block_diffs, "tiles": tile_diffs}

    @staticmethod
    def _meta_at(data, si):
        if not data:
            return 0
        idx = si >> 1
        if idx >= len(data):
            return 0
        return (data[idx] >> ((si & 1) << 2)) & 0x0F

    def iter_blocks(self, cx, cz, x0=None, z0=None, x1=None, z1=None,
                    y0=None, y1=None):
        """遍历本 chunk 内的非空气方块，产出**世界坐标** (x, y, z, block_id, meta)。

        cx/cz 是本 chunk 的 chunk 坐标，用于把局部坐标换算成世界坐标。
        传入边界可只遍历局部；不传则遍历整 chunk。
        """
        base_x = cx * 16
        base_z = cz * 16
        if x0 is not None:
            lx0, lx1 = max(x0 - base_x, 0), min(x1 - base_x, 15)
        else:
            lx0, lx1 = 0, 15
        if z0 is not None:
            lz0, lz1 = max(z0 - base_z, 0), min(z1 - base_z, 15)
        else:
            lz0, lz1 = 0, 15
        for sy, b in self._blocks.items():
            y_base = sy * 16
            for y in range(y_base, y_base + 16):
                if y0 is not None and not (y0 <= y <= y1):
                    continue
                for lz in range(lz0, lz1 + 1):
                    for lx in range(lx0, lx1 + 1):
                        si = self._index(lx, y, lz)
                        if si >= len(b):
                            continue
                        bid = b[si]
                        if bid == 0:
                            continue
                        meta = 0
                        d = self._data.get(sy)
                        if d:
                            idx = si >> 1
                            if idx < len(d):
                                meta = (d[idx] >> ((si & 1) << 2)) & 0x0F
                        yield base_x + lx, y, base_z + lz, bid, meta


def load_chunk(region, world, cx, cz):
    """从 world 读出一个 chunk 并包装成 Chunk 视图。"""
    data, *_ = region.read_chunk(world, cx, cz)
    return Chunk(data, cx=cx, cz=cz)


def scan_blocks(region, world, box):
    """批量扫描一个区域内的方块，返回 {(x,y,z): (id, meta)}。

    这是 chunk 级的批量读：每个 chunk 只解压一次，之后按需查询，
    避免逐点 read_block 造成的 O(n²)。
    """
    x0, z0, x1, z1 = box
    out = {}
    for cx in range(x0 >> 4, (x1 >> 4) + 1):
        for cz in range(z0 >> 4, (z1 >> 4) + 1):
            try:
                ch = load_chunk(region, world, cx, cz)
            except Exception:
                continue
            for x, y, z, bid, meta in ch.iter_blocks(cx, cz, x0, z0, x1, z1):
                out[(x, y, z)] = (bid, meta)
    return out
