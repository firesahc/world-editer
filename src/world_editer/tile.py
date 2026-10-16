"""Tile entity read/patch helpers (1.12 Java)."""
import copy
import struct
import zlib
from pathlib import Path

from . import region


def tile_at(world, x, y, z):
    cx, cz = x >> 4, z >> 4
    data, *_ = region.read_chunk(world, cx, cz)
    for te in region.parse_tile_entities(data):
        if (te.get("x"), te.get("y"), te.get("z")) == (x, y, z):
            return te
    return None


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
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    nb = sys.modules.get("nbt")
    if nb is None:
        import importlib
        nb = importlib.import_module("world_editer.nbt")
    # walk root compound's TileEntities list to find matching name field value
    root_name, comp, _ = nb.read_root(raw)
    lvl = comp
    if isinstance(lvl, dict) and "Level" in lvl:
        lvl = lvl["Level"][1] if isinstance(lvl["Level"], tuple) and lvl["Level"][0] == 10 else lvl["Level"]
    if not isinstance(lvl, dict):
        return None
    tes = lvl.get("TileEntities")
    if not (isinstance(tes, tuple) and tes[0] == (9 if False else 9)):
        return None
    # tes: ("list", sub=10, [compounds])
    _, sub, items = tes
    for te in items:
        if not isinstance(te, tuple) or te[0] != 10:
            continue
        d = te[1]
        if not isinstance(d, dict):
            continue
        if name in d and isinstance(d[name], tuple) and d[name][0] == 8:  # string
            return d[name][1]
    return None


def _patch_int(raw, field, new_int):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    nb = sys.modules.get("world_editer.nbt")
    if nb is None:
        import importlib
        nb = importlib.import_module("world_editer.nbt")
    return nb.patch_int(raw, field, new_int)


def tile_set(world, x, y, z, patch):
    cx, cz = x >> 4, z >> 4
    data, rf, li, sector, start, ln, raw = region.read_chunk(world, cx, cz)
    new = data
    for key, val in patch.items():
        if isinstance(val, str):
            cur = _find_string_field(new, key)
            if cur is None:
                raise KeyError(f"string field {key!r} not found")
            sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
            nb = __import__("world_editer.nbt", fromlist=["patch_field"])
            new = nb.patch_field(new, key, cur, val)
        elif isinstance(val, int):
            new = _patch_int(new, key, val)
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
