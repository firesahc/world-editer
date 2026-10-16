"""Terrain block id/name helpers (1.12 Java)."""
# 1.12 block ids (subset; full table TBD). Add as encountered.
BLOCKS_1_12 = {
    0: "air",
    1: "stone", 2: "grass", 3: "dirt", 4: "cobblestone", 5: "planks",
    7: "bedrock", 8: "water", 9: "water", 10: "lava", 11: "lava",
    12: "sand", 13: "gravel", 14: "gold_ore", 15: "iron_ore",
    16: "coal_ore", 17: "log", 18: "leaves", 19: "sponge",
    20: "glass", 21: "lapis_ore", 22: "lapis_block", 23: "dispenser",
    24: "sandstone", 26: "bed", 29: "sticky_piston", 30: "web",
    32: "deadbush", 33: "piston", 35: "wool", 37: "yellow_flower",
    38: "red_flower", 39: "brown_mushroom", 40: "red_mushroom",
    41: "gold_block", 42: "iron_block", 43: "double_stone_slab",
    44: "stone_slab", 45: "brick_block", 46: "tnt", 47: "bookshelf",
    48: "mossy_cobblestone", 49: "obsidian", 50: "torch", 51: "fire",
    52: "mob_spawner", 53: "oak_stairs", 54: "chest", 56: "diamond_ore",
    57: "diamond_block", 58: "crafting_table", 60: "farmland",
    61: "furnace", 62: "lit_furnace", 63: "standing_sign", 64: "wooden_door",
    65: "ladder", 66: "rail", 67: "stone_stairs", 68: "wall_sign",
    69: "lever", 73: "redstone_ore", 74: "lit_redstone_ore",
    75: "unlit_redstone_torch", 76: "redstone_torch",
    77: "stone_button", 78: "snow_layer", 79: "ice", 80: "snow",
    81: "cactus", 82: "clay", 83: "reeds", 84: "jukebox",
    85: "fence", 86: "pumpkin", 87: "netherrack", 88: "soul_sand",
    89: "glowstone", 90: "portal", 91: "lit_pumpkin", 95: "stained_glass",
    98: "stonebrick", 99: "brown_mushroom_block", 100: "red_mushroom_block",
    101: "iron_bars", 102: "glass_pane", 103: "melon_block", 109: "stone_brick_stairs",
    110: "mycelium", 112: "nether_brick", 113: "nether_brick_fence",
    114: "nether_brick_stairs", 116: "enchanting_table", 121: "end_stone",
    123: "redstone_lamp", 124: "lit_redstone_lamp",
    126: "wooden_slab", 129: "emerald_ore", 130: "ender_chest",
    133: "emerald_block", 139: "cobblestone_wall", 145: "anvil",
    152: "redstone_block", 153: "quartz_ore", 155: "quartz_block",
    156: "quartz_stairs", 157: "activator_rail", 160: "stained_glass_pane",
    170: "hay_block", 172: "hardened_clay", 173: "coal_block",
    19: "sponge", 61: "furnace",
}


def block_name(bid):
    return BLOCKS_1_12.get(bid, f"unknown_{bid}")


def read_block(world, x, y, z):
    cx, cz = x >> 4, z >> 4
    import struct
    from . import region
    data, *_ = region.read_chunk(world, cx, cz)
    # parse sections
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent.parent))
    nb = sys.modules.get("world_editer.nbt")
    if nb is None:
        import importlib
        nb = importlib.import_module("world_editer.nbt")
    _, comp, _ = nb.read_root(data)
    lvl = comp
    if isinstance(lvl, dict) and "Level" in lvl:
        lvl = lvl["Level"][1] if isinstance(lvl["Level"], tuple) and lvl["Level"][0] == 10 else lvl["Level"]
    if not isinstance(lvl, dict):
        return None
    sections = lvl.get("Sections")
    if not (isinstance(sections, tuple) and sections[0] == 9):
        return {"id": 0, "meta": 0, "name": "air (no section)"}
    inner = sections[1] if isinstance(sections,tuple) and len(sections)==2 else sections
    items = inner[2] if isinstance(inner,tuple) and len(inner)==3 else (inner[1] if isinstance(inner,tuple) else [])
    sy = y >> 4
    for sec in items:
        if not (isinstance(sec, tuple) and sec[0] == 10):
            continue
        sd = sec[1]
        if not isinstance(sd, dict):
            continue
        yoff = sd.get("Y")
        yv = yoff[1] if (isinstance(yoff, tuple)) else yoff
        if yv != sy:
            continue
        blocks = sd.get("Blocks")
        bdata = sd.get("Data")
        if not (isinstance(blocks, tuple) and blocks[0] == 7):
            return None
        _, bbytes = blocks
        si = ((y & 15) << 8) | ((z & 15) << 4) | (x & 15)
        bid = bbytes[si]
        meta = 0
        if isinstance(bdata, tuple) and bdata[0] == 7:
            bt = bdata[1]
            idx = si >> 1
            if idx < len(bt):
                meta = (bt[idx] >> ((si & 1) << 2)) & 0x0F
        return {"id": bid, "meta": meta, "name": block_name(bid)}
    return {"id": 0, "meta": 0, "name": "air (no section at y)"}
