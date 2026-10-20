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


# region 文件内容缓存：{绝对路径: (mtime, bytes)}
# 批量扫描时同一 region 会被读上百次，不缓存就是 O(n²) 的 IO 放大。
# 写入 region 后必须失效对应条目（见 _invalidate_region）。
_REGION_CACHE = {}


def _read_region_bytes(rf):
    """读 region 文件并缓存内容；文件被修改后自动失效。"""
    key = str(rf)
    try:
        st = rf.stat()
    except OSError:
        return b""
    sig = (st.st_mtime_ns, st.st_size)
    hit = _REGION_CACHE.get(key)
    if hit is not None and hit[0] == sig:
        return hit[1]
    raw = rf.read_bytes()
    _REGION_CACHE[key] = (sig, raw)
    return raw


def invalidate_region_cache(world=None):
    """清空缓存。写完 region 后应调用；world=None 清全部。"""
    if world is None:
        _REGION_CACHE.clear()
        return
    pref = str(Path(world).resolve())
    for k in list(_REGION_CACHE):
        if k.startswith(pref):
            del _REGION_CACHE[k]


def chunk_location(world, cx, cz):
    rx, rz = cx >> 5, cz >> 5
    rf = Path(world) / "region" / f"r.{rx}.{rz}.mca"
    if not rf.exists():
        raise FileNotFoundError(f"region 文件不存在: {rf}")
    li = (cz - rz * 32) * 32 + (cx - rx * 32)
    raw = _read_region_bytes(rf)
    off = struct.unpack(">I", raw[li * 4:li * 4 + 4])[0]
    if off == 0:
        raise KeyError(f"chunk 尚未生成: cx={cx} cz={cz}")
    sector = off >> 8
    if sector == 0:
        raise KeyError(f"chunk location 为空: cx={cx} cz={cz}")
    return rf, li, sector, raw


def decompress_chunk_payload(raw, start, nsec, ln):
    """Robustly decompress a 1.12 Anvil chunk payload.

    Minecraft stores ``L`` in the header but some worlds/edits under-report it;
    the allocated ``nsec`` sectors always carry the complete stream, so fall back
    to scanning the whole sector range when the declared size is too short.
    """
    if nsec and nsec > 0:
        sector_end = start + nsec * 4096
    else:
        sector_end = start + ln + 4095
    if sector_end > len(raw):
        sector_end = len(raw)
    # Full sector range (includes trailing padding).
    full = raw[start + 5:sector_end]
    # Declared range (exclusive upper bound from header).
    if ln and ln >= 1:
        declared_end = min(start + 5 + (ln - 1), len(raw))
        declared = raw[start + 5:declared_end]
    else:
        declared = b""
    for blob in (full, declared):
        if not blob:
            continue
        try:
            dec = zlib.decompress(blob)
            return dec
        except Exception:
            pass
        obj = zlib.decompressobj()
        try:
            dec = obj.decompress(blob)
        except Exception:
            continue
        # Accept only when the stream is actually complete, else try the
        # other slice.
        if obj.eof:
            return dec
    # Last resort: decompressobj without EOF requirement on the fullest slice.
    obj = zlib.decompressobj()
    dec = obj.decompress(full)
    if not dec:
        raise ValueError("chunk payload could not be decompressed")
    return dec


def read_chunk(world, cx, cz):
    rf, li, sector, raw = chunk_location(world, cx, cz)
    start = sector * 4096
    ln = struct.unpack(">I", raw[start:start + 4])[0]
    nsec = (ln + 4095) // 4096 if ln else 0
    loc = struct.unpack(">I", raw[li * 4:li * 4 + 4])[0]
    nsec = loc & 0xFF or nsec
    t = raw[start + 4]
    if t != 2:
        raise ValueError(f"非 zlib 压缩 (type={t})")
    data = decompress_chunk_payload(raw, start, nsec, ln)
    return data, rf, li, sector, start, ln, raw


def write_chunk(world, cx, cz, new_nbt_bytes):
    rf, li, sector, raw = chunk_location(world, cx, cz)
    raw = bytearray(raw)
    start = sector * 4096
    # 该 chunk 实际占用的扇区数：位置表里的低字节是权威值
    # （read_chunk 同样优先用它），不能只信头部长度字段。
    loc = struct.unpack(">I", raw[li * 4:li * 4 + 4])[0]
    nsec = loc & 0xFF
    if not nsec:
        nsec = (struct.unpack(">I", raw[start:start + 4])[0] + 4095) // 4096
    compressed = zlib.compress(new_nbt_bytes)
    # 头部长度字段 = 压缩后长度 + 1（+1 是 compressionType 字节）。
    # 这里曾经写成未压缩长度，导致头部声称的扇区数远大于实际占用，
    # 下一次 inplace 写入的零填充会抹掉后续 chunk 的数据。
    payload = struct.pack(">I", len(compressed) + 1) + b"\x02" + compressed
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
    invalidate_region_cache(world)
    return {"path": str(rf), "mode": mode, "old_sectors": nsec, "new_sectors": need}


def backup_region(world, region_path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = Path(world) / "backups" / ts
    outdir.mkdir(parents=True, exist_ok=True)
    dst = outdir / Path(region_path).name
    shutil.copy2(region_path, dst)
    return dst


def _unwrap(v):
    """保留的薄封装：形态判别的唯一实现在 nbt.unwrap()。"""
    return nb.unwrap(v)


def parse_tile_entities(data):
    """已废弃：改用 chunk.Chunk(data).tiles()。

    保留仅为兼容旧调用；chunk 层是 tile 解析的唯一归属。
    """
    from . import chunk as ck
    return ck.Chunk(data).tiles()


# ------------------------------------------------------------------ 比对

def mca_files(path):
    """把一个路径归一成 {文件名: .mca 路径}。

    接受：单个 .mca 文件 / 含 .mca 的目录 / 世界根目录（含 region/）。
    """
    p = Path(path)
    if p.is_file():
        return {p.name: p}
    if (p / "region").is_dir():
        p = p / "region"
    if not p.is_dir():
        raise FileNotFoundError("not a .mca file or directory: %s" % path)
    return {f.name: f for f in sorted(p.glob("*.mca"))}


def _chunks_in_file(rf):
    """产出 (cx, cz, chunk_nbt_bytes)。"""
    raw = rf.read_bytes()
    try:
        _, rx, rz = rf.stem.split(".")
        rx, rz = int(rx), int(rz)
    except ValueError:
        return []
    out = []
    for li in range(1024):
        off = struct.unpack(">I", raw[li * 4:li * 4 + 4])[0]
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
            data = decompress_chunk_payload(raw, start, count, ln)
        except Exception:
            continue
        out.append((rx * 32 + (li % 32), rz * 32 + (li // 32), data))
    return out


def diff_files(a_path, b_path):
    """比较两个 .mca 文件的 chunk 级差异（before → after）。"""
    from . import chunk as ck
    # 键必须是 (cx, cz)：一个 region 文件里同一个 cx 对应 32 个不同 cz，
    # 只按 cx 建表会把上千个 chunk 压成 32 个。
    ca = {(cx, cz): d for cx, cz, d in _chunks_in_file(Path(a_path))}
    cb = {(cx, cz): d for cx, cz, d in _chunks_in_file(Path(b_path))}
    chunks = []
    for key in sorted(set(ca) | set(cb)):
        cx, cz = key
        a = ca.get(key)
        b = cb.get(key)
        if a is None or b is None:
            chunks.append({
                "cx": cx, "cz": cz,
                "status": "added" if b is not None else "removed",
                "blocks": [], "tiles": [],
            })
            continue
        d = ck.Chunk(a, cx=cx, cz=cz).diff(ck.Chunk(b, cx=cx, cz=cz))
        if d["blocks"] or d["tiles"]:
            chunks.append({"cx": cx, "cz": cz, "status": "changed", **d})
    return chunks


def diff_worlds(before_path, after_path):
    """比较两个世界/目录/文件（before → after），返回带汇总的差异报告。

    噪声字段（LastUpdate / HeightMap / LastOutput 等）在 chunk 层已过滤。
    """
    fa = mca_files(before_path)
    fb = mca_files(after_path)
    files = []
    summary = {"files_compared": 0, "files_only_before": 0, "files_only_after": 0,
               "chunks_changed": 0, "blocks_changed": 0, "tiles_changed": 0}
    for name in sorted(set(fa) | set(fb)):
        if name not in fa:
            summary["files_only_after"] += 1
            files.append({"name": name, "status": "added", "chunks": []})
            continue
        if name not in fb:
            summary["files_only_before"] += 1
            files.append({"name": name, "status": "removed", "chunks": []})
            continue
        summary["files_compared"] += 1
        chunks = diff_files(fa[name], fb[name])
        if chunks:
            files.append({"name": name, "status": "changed", "chunks": chunks})
            summary["chunks_changed"] += len(chunks)
            for c in chunks:
                summary["blocks_changed"] += len(c.get("blocks", []))
                summary["tiles_changed"] += len(c.get("tiles", []))
    return {"files": files, "summary": summary}
