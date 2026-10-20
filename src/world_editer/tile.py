"""Tile entity read/patch helpers (1.12 Java)."""
import struct
import sys
from pathlib import Path

from . import region


def tile_at(world, x, y, z):
    """按块坐标精确定位 TileEntity。定位逻辑统一走 chunk 层。"""
    from . import chunk as ck
    try:
        ch = ck.load_chunk(region, world, x >> 4, z >> 4)
    except Exception:
        return None
    return ch.tile_at(x, y, z)


def encode_patch(raw_chunk_nbt, patch):
    """Apply a dict of field->value patch onto raw chunk nbt bytes.
       Supported value types: str (full-replace string field), int (full-replace int field)."""
    out = raw_chunk_nbt
    for key, val in patch.items():
        if isinstance(val, str):
            # find current value by locating field name in nbt
            cur = _find_string_field(out, key)
            if cur is None:
                raise KeyError(f"string field {key!r} not found")
            out = _nbt_patch_field(out, key, cur, val) if (cur_val := cur) else out
            # use region patch helper instead:
            # revert and use low-level bytes replace via region function shim
        elif isinstance(val, int):
            cur = _find_int_field(out, key)
            if cur is None:
                raise KeyError(f"int field {key!r} not found")
            out = _patch_int(out, key, val)
        else:
            raise ValueError(f"unsupported patch type {type(val)} for {key!r}")
    return out


def _find_string_field(raw, name):
    """在 chunk NBT 中找出名为 name 的 TagString 字段的值（不限定 tile）。

    形态判别统一走 nbt 的访问器（这层判别曾经因各写各的而出过 bug）。
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    nb = sys.modules.get("world_editer.nbt")
    if nb is None:
        import importlib
        nb = importlib.import_module("world_editer.nbt")
    _, comp, _ = nb.read_root(raw)
    lvl = nb.as_compound(comp)
    if lvl is None:
        return None
    lvl = nb.as_compound(lvl.get("Level")) or lvl
    tes = nb.as_list(lvl.get("TileEntities"))
    if tes is None:
        return None
    for te in tes:
        d = nb.as_compound(te)
        if d is None:
            continue
        v = d.get(name)
        if isinstance(v, tuple) and len(v) == 2 and v[0] == 8:  # TAG_STRING
            return v[1]
    return None


def _nbt():
    """取 world_editer.nbt 模块（包内相对导入，避免依赖 sys.path 顺序）。"""
    from . import nbt
    return nbt


def _iter_tile_compounds(raw):
    """产出 chunk NBT 中每个 TileEntity 的 compound，字段值已解包。

    值经 nbt.unwrap 归一为朴素 Python，因此 x/y/z 是裸 int、
    Command 是裸 str —— 定位与比较都按朴素值做。
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    nb = sys.modules.get("world_editer.nbt")
    if nb is None:
        import importlib
        nb = importlib.import_module("world_editer.nbt")
    _, comp, _ = nb.read_root(raw)
    lvl = nb.as_compound(comp)
    if lvl is None:
        return
    lvl = nb.as_compound(lvl.get("Level")) or lvl
    tes = nb.as_list(lvl.get("TileEntities"))
    if tes is None:
        return
    for te in tes:
        d = nb.as_compound(te)
        if d is None:
            continue
        yield {k: nb.unwrap(v) for k, v in d.items()}


def _find_string_field_at(raw, name, x, y, z):
    """找出**指定坐标**那个 tile 上的字符串字段值。"""
    for d in _iter_tile_compounds(raw):
        if d.get("x") == x and d.get("y") == y and d.get("z") == z:
            v = d.get(name)
            if isinstance(v, str):
                return v
    return None


def _patch_int_at(raw, field, new_int, x, y, z):
    """把**指定坐标**那个 tile 上的 int 字段改掉。

    旧实现用 `raw.find(marker)` 取全 chunk 首次匹配，会打到别的 tile 上。
    这里改为：先确认目标 tile 上该字段存在，再检查该字段名在整个 chunk 内
    是否唯一；不唯一就拒绝修改（宁可不改，也不要改错对象）。
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    nb = sys.modules.get("world_editer.nbt")
    if nb is None:
        import importlib
        nb = importlib.import_module("world_editer.nbt")

    found = False
    for d in _iter_tile_compounds(raw):
        if d.get("x") == x and d.get("y") == y and d.get("z") == z:
            v = d.get(field)
            if isinstance(v, int) and not isinstance(v, bool):
                found = True
            break
    if not found:
        raise KeyError(f"int field {field!r} not found on tile at {(x, y, z)}")

    # 统计该字段名在整个 chunk 里的出现次数，确保字节替换不会命中别的 tile
    tag_name = field.encode("utf-8")
    marker = bytes([nb.TAG_INT]) + struct.pack(">H", len(tag_name)) + tag_name
    occurrences = raw.count(marker)
    if occurrences != 1:
        raise ValueError(
            f"int field {field!r} occurs {occurrences} times in this chunk; "
            f"refusing an ambiguous in-place patch")
    return nb.patch_int(raw, field, new_int)


def _patch_int(raw, field, new_int):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    nb = sys.modules.get("world_editer.nbt")
    if nb is None:
        import importlib
        nb = importlib.import_module("world_editer.nbt")
    return nb.patch_int(raw, field, new_int)


def tile_set(world, x, y, z, patch):
    """合并式修改**指定坐标**的那个 TileEntity。

    与旧实现的区别：补丁被定位到 x/y/z 对应的**那一个** tile，
    而不是对整个 chunk 做字符串替换 —— 同 chunk 内存在同名字段时
    旧实现会报错或打到别的对象上。
    """
    cx, cz = x >> 4, z >> 4
    data, rf, li, sector, start, ln, raw = region.read_chunk(world, cx, cz)
    new = data
    for key, val in patch.items():
        if isinstance(val, str):
            cur = _find_string_field_at(new, key, x, y, z)
            if cur is None:
                raise KeyError(
                    f"string field {key!r} not found on tile at {(x, y, z)}")
            nb = _nbt()
            # 字节级替换只能定位到"字段名+旧值"这一组字节；若整个 chunk 里
            # 出现多次，替换会命中错误的 tile。此时明确拒绝，而不是乱改。
            pat = (bytes([nb.TAG_STRING])
                   + struct.pack(">H", len(key.encode("utf-8")))
                   + key.encode("utf-8")
                   + struct.pack(">H", len(cur.encode("utf-8")))
                   + cur.encode("utf-8"))
            n = new.count(pat)
            if n != 1:
                raise ValueError(
                    f"string field {key!r} with value {cur!r} occurs {n} times "
                    f"in chunk ({cx},{cz}); refusing an ambiguous in-place patch")
            new = nb.patch_field(new, key, cur, val)
        elif isinstance(val, int):
            new = _patch_int_at(new, key, val, x, y, z)
        else:
            raise ValueError(f"unsupported patch type {type(val)} for {key!r}")
    # backup
    bp = region.backup_region(world, rf)
    region.write_chunk(world, cx, cz, new)
    return {"coords": (x, y, z), "backup": str(bp), "patched": list(patch.keys())}


def tile_delete(world, x, y, z):
    # 1.12: delete = tile entity compound removal is non-trivial; leave as not-supported
    raise NotImplementedError("tile_delete not implemented for 1.12 (use set to air+empty)")

def tile_list(world, box=None, keyword=None):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from world_editer import region
    out = []
    # box: (x1,z1,x2,z2) in block coords; if None scan all loaded chunks
    if box is None:
        # scan region files header
        for rf in sorted((Path(world) / "region").glob("*.mca")):
            raw = rf.read_bytes()
            for i in range(1024):
                off = struct.unpack(">I", raw[i * 4:i * 4 + 4])[0]
                if off == 0:
                    continue
                sector = off >> 8
                if sector == 0:
                    continue
                count = off & 0xFF
                start = sector * 4096
                if start + 5 > len(raw) or raw[start + 4] != 2:
                    continue
                ln = struct.unpack(">I", raw[start:start + 4])[0]
                try:
                    data = region.decompress_chunk_payload(raw, start, count, ln)
                except Exception:
                    continue
                for te in region.parse_tile_entities(data):
                    if keyword and keyword not in (te.get("Command") or "") and keyword not in (te.get("id") or ""):
                        continue
                    out.append(te)
    else:
        x1, z1, x2, z2 = box
        cx1, cz1 = x1 >> 4, z1 >> 4
        cx2, cz2 = x2 >> 4, z2 >> 4
        for cx in range(cx1, cx2 + 1):
            for cz in range(cz1, cz2 + 1):
                try:
                    data, *_ = region.read_chunk(world, cx, cz)
                except Exception:
                    continue
                for te in region.parse_tile_entities(data):
                    if not (x1 <= te.get("x", 0) <= x2 and z1 <= te.get("z", 0) <= z2):
                        continue
                    if keyword and keyword not in (te.get("Command") or "") and keyword not in (te.get("id") or ""):
                        continue
                    out.append(te)
    return out
