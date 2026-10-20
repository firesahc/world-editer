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
    """一个已加载的 1.12 chunk 的只读视图。

    构造一次、多次查询，避免逐点重读 chunk（逐点 read_block 是 O(n²)）。
    """

    __slots__ = ("_tiles", "_sections", "_blocks", "_data", "_sy")

    def __init__(self, nbt_bytes: bytes):
        _, comp, _ = nb.read_root(nbt_bytes)
        lvl = nb.as_compound(comp)
        if lvl is None:
            lvl = {}
        else:
            lvl = nb.as_compound(lvl.get("Level")) or lvl

        self._tiles = self._parse_tiles(lvl)
        self._sections = nb.as_list(lvl.get("Sections")) or []
        # section Y -> (Blocks bytes, Data bytes)
        self._blocks = {}
        self._data = {}
        self._sy = {}
        for sec in self._sections:
            sd = nb.as_compound(sec)
            if sd is None:
                continue
            sy = nb.unwrap(sd.get("Y"))
            if not isinstance(sy, int):
                continue
            self._sy[sy] = sd
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
    return Chunk(data)


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
