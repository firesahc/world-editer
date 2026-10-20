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


def cmd_set_block(args):
    w = _world(args)
    res = block.set_block(w, args.x, args.y, args.z, args.block, args.meta,
                          backup=not args.no_backup)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


def cmd_fill(args):
    w = _world(args)
    box = (args.x1, args.y1, args.z1, args.x2, args.y2, args.z2)
    res = block.fill_area(w, box, args.block, args.meta,
                          only_air=args.only_air, dry_run=args.dry_run,
                          max_blocks=args.max_blocks, backup=not args.no_backup)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


def cmd_diff(args):
    w = _world(args)
    after = args.after or w
    res = region.diff_worlds(args.before, after)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    s = res["summary"]
    print("对比: %s  ->  %s" % (args.before, after))
    print("文件: 比较 %d, 仅前有 %d, 仅后有 %d" % (
        s["files_compared"], s["files_only_before"], s["files_only_after"]))
    print("变更: chunk %d, 方块 %d, tile字段 %d" % (
        s["chunks_changed"], s["blocks_changed"], s["tiles_changed"]))
    for f in res["files"]:
        if f["status"] != "changed":
            print("  [%s] %s" % (f["status"], f["name"]))
            continue
        for c in f["chunks"]:
            print("  %s chunk(%s,%s) %s" % (
                f["name"], c["cx"], c["cz"], c["status"]))
            for b in c["blocks"][:50]:
                print("     block %s  %s -> %s" % (b["pos"], b["before"], b["after"]))
            for t in c["tiles"][:50]:
                print("     tile  %s.%s  %r -> %r" % (
                    t["pos"], t["field"], t["before"], t["after"]))
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

    sb = s2.add_parser("block", help="set a terrain block")
    for a in ("world", "x", "y", "z"):
        sb.add_argument(f"--{a}" if a != "world" else "-w", dest=a, required=True, type=str if a == "world" else int)
    sb.add_argument("block", help="block name (e.g. stone) or id")
    sb.add_argument("--meta", type=int, default=0)
    sb.add_argument("--no-backup", action="store_true")
    sb.set_defaults(func=cmd_set_block)

    lst = sub.add_parser("list", help="list tile entities")
    lst.add_argument("-w", "--world", required=True, dest="world")
    lst.add_argument("--box", default=None)
    lst.add_argument("--keyword", default=None)
    lst.set_defaults(func=cmd_list_tiles)

    fl = sub.add_parser("fill", help="fill a box with a block")
    fl.add_argument("-w", "--world", required=True, dest="world")
    for a in ("x1", "y1", "z1", "x2", "y2", "z2"):
        fl.add_argument(f"--{a}", dest=a, required=True, type=int)
    fl.add_argument("block", help="block name (e.g. stone) or id")
    fl.add_argument("--meta", type=int, default=0)
    fl.add_argument("--only-air", action="store_true",
                    help="only fill air, keep existing blocks")
    fl.add_argument("--dry-run", action="store_true",
                    help="report what would change without writing")
    fl.add_argument("--max-blocks", type=int, default=1_000_000)
    fl.add_argument("--no-backup", action="store_true")
    fl.set_defaults(func=cmd_fill)

    df = sub.add_parser("diff", help="compare two world states")
    df.add_argument("-w", "--world", required=True, dest="world")
    df.add_argument("--before", required=True,
                    help="backup dir / .mca file / world root (the 'before' side)")
    df.add_argument("--after", default=None,
                    help="the 'after' side; defaults to --world")
    df.add_argument("--json", action="store_true")
    df.set_defaults(func=cmd_diff)

    bk = sub.add_parser("backup", help="backup whole region")
    bk.add_argument("-w", "--world", required=True, dest="world")
    bk.add_argument("--label", default=None)
    bk.set_defaults(func=cmd_backup)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
