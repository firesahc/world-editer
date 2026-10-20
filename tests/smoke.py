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

    # 4. block read 必须在已知命令方块坐标上返回真实 id（不是空气）
    #    曾经的弱断言 isinstance(dict) 掩盖了 read_block 恒返回空气的 bug
    cmd_tiles = [t for t in tile.tile_list(WORLD, keyword=None)
                 if "Command" in t]
    assert cmd_tiles, "no command block tiles found"
    checked = 0
    for t in cmd_tiles[:20]:
        b = block.read_block(WORLD, t["x"], t["y"], t["z"])
        assert b["id"] in (137, 210, 211), (
            "read_block(%s,%s,%s) -> %s, expected a command block id"
            % (t["x"], t["y"], t["z"], b))
        checked += 1
    print("read_block hits command blocks:", checked)

    # 5. BLOCKS_1_12 必须覆盖 1.12 关键方块
    for bid, name in ((55, "redstone_wire"), (93, "unpowered_repeater"),
                      (137, "command_block"), (149, "unpowered_comparator"),
                      (152, "redstone_block"), (210, "repeating_command_block"),
                      (211, "chain_command_block")):
        assert block.block_name(bid) == name, (
            "BLOCKS_1_12[%d] should be %s, got %s"
            % (bid, name, block.block_name(bid)))
    print("BLOCKS_1_12 key entries ok")

    # 6. nbt 访问器：双层 byte array、裸 dict section、异构 list
    import world_editer.nbt as nb
    assert nb.as_bytes((7, ("bytearray", b"\x01\x02"))) == b"\x01\x02"
    assert nb.as_compound({"a": 1}) == {"a": 1}
    assert nb.as_list(("list", 10, [1, 2])) == [1, 2]
    assert nb.unwrap((1, 0)) == 0
    print("nbt accessors ok")

    print("SMOKE PASS")

if __name__ == "__main__":
    main()
