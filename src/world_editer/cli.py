"""CLI for world-editer (argparse, pure stdlib)."""
import argparse
import json
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent.parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from world_editer import tile, block, region


def _world(args):
    return Path(args.world).resolve()


def cmd_get_tile(args):
    w = _world(args)
    te = tile.tile_at(w, args.x, args.y, args.z)
    if te is None:
        print(json.dumps({"found": False, "coords": [args.x, args.y, args.z]}, ensure_ascii=False))
        return 1
    out = {k: (list(v) if isinstance(v, tuple) else v) for k, v in te.items()}
    out["found"] = True
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_set_tile(args):
    w = _world(args)
    patch = json.loads(Path(args.patch).read_text(encoding="utf-8"))
    res = tile.tile_set(w, args.x, args.y, args.z, patch)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


def cmd_get_block(args):
    w = _world(args)
    print(json.dumps(block.read_block(w, args.x, args.y, args.z), ensure_ascii=False, indent=2))
    return 0


def cmd_list_tiles(args):
    w = _world(args)
    box = None
    if args.box:
        parts = [int(p) for p in args.box.split(",")]
        if len(parts) == 4:
            box = (parts[0], parts[1], parts[2], parts[3])
        elif len(parts) == 6:
            box = (parts[0], parts[2], parts[3], parts[5])
    res = tile.tile_list(w, box=box, keyword=args.keyword)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


def cmd_backup(args):
    w = _world(args)
    import glob
    rf = None
    # backup all region files in world/region
    outdir = Path(w) / "backups" / ( Path(args.label).name if args.label else datetime_now() )
    outdir.mkdir(parents=True, exist_ok=True)
    for f in sorted((w / "region").glob("*.mca")):
        dst = outdir / f.name
        import shutil
        shutil.copy2(f, dst)
    print(str(outdir))


def datetime_now():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def main():
    ap = argparse.ArgumentParser(prog="world-editer", description="Minecraft 1.12 world data editor (CLI)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("get", help="read data")
    g2 = g.add_subparsers(dest="what", required=True)
    gt = g2.add_parser("tile")
    for a in ("world", "x", "y", "z"):
        gt.add_argument(f"--{a}" if a != "world" else "-w" if a == "world" else f"--{a}", dest=a, required=True, type=int if a != "world" else str)
    gt.set_defaults(func=cmd_get_tile)

    gb = g2.add_parser("block")
    for a in ("world", "x", "y", "z"):
        gb.add_argument(f"--{a}" if a != "world" else "-w", dest=a, required=True, type=int if a != "world" else str)
    gb.set_defaults(func=cmd_get_block)

    s = sub.add_parser("set", help="patch data")
    s2 = s.add_subparsers(dest="what", required=True)
    st = s2.add_parser("tile")
    for a in ("world", "x", "y", "z", "patch"):
        st.add_argument(f"--{a}" if a != "world" else "-w", dest=a, required=True, type=str if a in ("world", "patch") else int)
    st.set_defaults(func=cmd_set_tile)

    lst = sub.add_parser("list", help="list tile entities")
    lst.add_argument("-w", "--world", required=True, dest="world")
    lst.add_argument("--box", default=None)
    lst.add_argument("--keyword", default=None)
    lst.set_defaults(func=cmd_list_tiles)

    bk = sub.add_parser("backup", help="backup whole region")
    bk.add_argument("-w", "--world", required=True, dest="world")
    bk.add_argument("--label", default=None)
    bk.set_defaults(func=cmd_backup)

    args = ap.parse_args()
    sys.exit(args.func(args))
