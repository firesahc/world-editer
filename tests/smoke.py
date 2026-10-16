"""Smoke tests for world-editer (no third-party deps)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from world_editer import tile, block, region

WORLD = ROOT / "tests" / "world"

def main():
    # 1. parse every .mca file under tests/world/region
    files = sorted((WORLD / "region").glob("*.mca"))
    assert files, "no test region files"
    total_chunks = 0
    total_tiles = 0
    parse_errors = 0
    for f in files:
        raw = f.read_bytes()
        for i in range(1024):
            off = __import__("struct").unpack(">I", raw[i*4:i*4+4])[0]
            if off == 0:
                continue
            sector = off >> 8
            if sector == 0:
                continue
            start = sector * 4096
            import struct, zlib
            ln = struct.unpack(">I", raw[start:start+4])[0]
            if raw[start+4] != 2:
                continue
            nsec = off & 0xFF
            try:
                data = region.decompress_chunk_payload(raw, start, nsec, ln)
            except Exception:
                continue
            try:
                tes = region.parse_tile_entities(data)
            except Exception:
                parse_errors += 1
                continue
            total_chunks += 1
            total_tiles += len(tes)
    print(f"解析 {len(files)} 个 .mca 文件, {total_chunks} chunks, {total_tiles} tiles, errors={parse_errors}")
    assert parse_errors == 0

    # 2. read a known tile if any
    sample_te = None
    for f in files:
        raw = f.read_bytes()
        # find first chunk with tile entities
        for i in range(1024):
            off = struct.unpack(">I", raw[i*4:i*4+4])[0]
            if off == 0: continue
            sector = off >> 8
            if sector == 0: continue
            start = sector * 4096
            ln = struct.unpack(">I", raw[start:start+4])[0]
            if raw[start+4] != 2: continue
            nsec = off & 0xFF
            try:
                data = region.decompress_chunk_payload(raw, start, nsec, ln)
            except Exception:
                continue
            tes = region.parse_tile_entities(data)
            if tes:
                sample_te = tes[0]
                break
        if sample_te:
            break
    assert sample_te is not None
    print("tile sample:", sample_te.get("id"), (sample_te.get("Command") or "")[:60])

    # 3. list_tiles via box on test world (use first file's coords)
    # just ensure function runs
    lst = tile.tile_list(WORLD, keyword="function")
    print("list function tiles:", len(lst))
    assert isinstance(lst, list)

    # 4. block read sanity on first chunk's tile x/y/z if present
    if sample_te and all(k in sample_te for k in ("x", "y", "z")):
        b = block.read_block(WORLD, sample_te["x"], sample_te["y"], sample_te["z"])
        print("block at tile:", b)
        assert isinstance(b, dict) and "id" in b

    print("SMOKE PASS")

if __name__ == "__main__":
    main()
