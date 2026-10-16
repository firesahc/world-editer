"""MCP server exposing world-editer as tools (fastmcp)."""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
if str(HERE / "src") not in sys.path:
    sys.path.insert(0, str(HERE / "src"))

from world_editer import tile, block, region

try:
    from fastmcp import FastMCP
    mcp = FastMCP("world-editer")
except Exception:
    mcp = None

WORLD = None


def set_world(p):
    global WORLD
    WORLD = Path(p).resolve()


def _w():
    if WORLD is None:
        raise RuntimeError("world not set; pass --world")
    return WORLD


if mcp is not None:
    @mcp.tool()
    async def get_tile(x: int, y: int, z: int) -> dict:
        """Read tile entity at (x,y,z) as JSON."""
        te = tile.tile_at(_w(), x, y, z)
        if te is None:
            return {"found": False, "coords": [x, y, z]}
        return {"found": True, "coords": [x, y, z], **{k: (list(v) if isinstance(v, tuple) else v) for k, v in te.items()}}

    @mcp.tool()
    async def set_tile(x: int, y: int, z: int, patch_json: str) -> dict:
        """Patch tile fields (merge). patch_json is JSON object of field->value."""
        patch = json.loads(patch_json)
        return tile.tile_set(_w(), x, y, z, patch)

    @mcp.tool()
    async def get_block(x: int, y: int, z: int) -> dict:
        """Read terrain block at (x,y,z): id, meta, name."""
        return block.read_block(_w(), x, y, z)

    @mcp.tool()
    async def list_tiles(keyword: str = "", x1: int = 0, z1: int = 0, x2: int = 0, z2: int = 0) -> list:
        """List tile entities in box [x1,z1]-[x2,z2], filter by keyword."""
        box = (x1, z1, x2, z2) if (x1 or z1 or x2 or z2) else None
        return tile.tile_list(_w(), box=box, keyword=keyword or None)

    @mcp.tool()
    async def backup(label: str = "") -> str:
        """Backup all region .mca files into world/backups/<timestamp>."""
        import shutil
        from datetime import datetime
        w = _w()
        ts = label or datetime.now().strftime("%Y%m%d_%H%M%S")
        out = w / "backups" / ts
        out.mkdir(parents=True, exist_ok=True)
        for f in sorted((w / "region").glob("*.mca")):
            shutil.copy2(f, out / f.name)
        return str(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", "-w", required=True)
    ap.add_argument("--transport", default="stdio")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    set_world(args.world)
    if mcp is None:
        print("fastmcp not installed: pip install fastmcp", file=__import__("sys").stderr)
        raise SystemExit(2)
    mcp.run(transport=args.transport, port=args.port)


if __name__ == "__main__":
    main()
