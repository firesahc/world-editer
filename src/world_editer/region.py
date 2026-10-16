"""Region (.mca) open + sector read/write + backup + tile parse (1.12 Java)."""
import os
import struct
import sys
import zlib
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
import world_editer.nbt as nb


def chunk_location(world, cx, cz):
    rx, rz = cx >> 5, cz >> 5
    rf = Path(world) / "region" / f"r.{rx}.{rz}.mca"
    if not rf.exists():
        raise FileNotFoundError(f"region 文件不存在: {rf}")
    li = (cz - rz * 32) * 32 + (cx - rx * 32)
    raw = rf.read_bytes()
    off = struct.unpack(">I", raw[li * 4:li * 4 + 4])[0]
    if off == 0:
        raise KeyError(f"chunk 尚未生成: cx={cx} cz={cz}")
    sector = off >> 8
    if sector == 0:
        raise KeyError(f"chunk location 为空: cx={cx} cz={cz}")
    return rf, li, sector, raw


def read_chunk(world, cx, cz):
    rf, li, sector, raw = chunk_location(world, cx, cz)
    start = sector * 4096
    ln = struct.unpack(">I", raw[start:start + 4])[0]
    t = raw[start + 4]
    if t != 2:
        raise ValueError(f"非 zlib 压缩 (type={t})")
    return zlib.decompress(raw[start + 5:start + 5 + ln - 1]), rf, li, sector, start, ln, raw


def write_chunk(world, cx, cz, new_nbt_bytes):
    rf, li, sector, raw = chunk_location(world, cx, cz)
    raw = bytearray(raw)
    start = sector * 4096
    ln = struct.unpack(">I", raw[start:start + 4])[0]
    nsec = (ln + 4095) // 4096
    payload = struct.pack(">I", len(new_nbt_bytes) + 1) + b"\x02" + zlib.compress(new_nbt_bytes)
    need = (len(payload) + 4095) // 4096
    if need <= nsec:
        mode = "inplace"
        raw[start:start + len(payload)] = payload
        for k in range(len(payload), nsec * 4096):
            raw[start + k] = 0
    else:
        mode = "alloc"
        nend = (len(raw) + 4095) // 4096
        while len(raw) < (nend + need) * 4096:
            raw.extend(b"\x00" * 4096)
        endstart = nend * 4096
        raw[endstart:endstart + len(payload)] = payload
        for k in range(len(payload), need * 4096):
            raw[endstart + k] = 0
        raw[li * 4:li * 4 + 4] = struct.pack(">I", (nend << 8) | need)
    rf.write_bytes(bytes(raw))
    return {"path": str(rf), "mode": mode, "old_sectors": nsec, "new_sectors": need}


def backup_region(world, region_path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = Path(world) / "backups" / ts
    outdir.mkdir(parents=True, exist_ok=True)
    dst = outdir / Path(region_path).name
    shutil.copy2(region_path, dst)
    return dst


def _unwrap(v):
    if isinstance(v, tuple):
        if len(v) == 2:
            return v[1]
        if len(v) == 3 and v[0] == 9:  # list -> items
            return [_unwrap(x) for x in v[2]]
    return v


def parse_tile_entities(data):
    _, comp, _ = nb.read_root(data)
    lvl = comp
    if isinstance(lvl, dict) and "Level" in lvl:
        v = lvl["Level"]
        lvl = v[1] if isinstance(v, tuple) and v[0] == 10 else v
    if not isinstance(lvl, dict):
        return []
    tes = lvl.get("TileEntities")
    if not (isinstance(tes, tuple) and tes[0] == 9):
        return []
    # tes is (9, ("list", sub, [items]))
    inner = tes[1]
    if isinstance(inner, tuple) and len(inner) == 3:
        items = inner[2]
    elif isinstance(tes, tuple) and len(tes) == 3:
        items = tes[2]
    else:
        items = []
    out = []
    for it in items:
        if isinstance(it, dict):
            d = it
        elif isinstance(it, tuple) and it[0] == 10 and isinstance(it[1], dict):
            d = it[1]
        else:
            continue
        attrs = {}
        for k, v in d.items():
            attrs[k] = _unwrap(v)
        out.append(attrs)
    return out
