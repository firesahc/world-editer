---
name: world-editer
description: 离线 Minecraft 1.12 Anvil（.mca）地图数据编辑操作——读取 TileEntity、编辑 command/sign/chest NBT、修改 terrain block 的 ID/data、backup/diff、所有操作都不需要反复手写 .py 脚本。只要你需要检查或修补 world/region/*.mca 中的数据时就用它。
---

# Skill: world-editer

## 何时调用

- 用户想要读取 x,y,z 处命令方块/告示牌/箱子的内容
- 用户想要修改命令方块命令 / 名字
- 用户想要检查或修补 x,y,z 处的 terrain block
- 用户想要在某区域内查找包含关键词的所有方块
- 用户要确认“我的修改是否真正改变了世界”（回归验证）
- 用户要求先备份再动 world

## 工具优先级

优先用 MCP 服务器 `world-editer`（在 opencode.jsonc 里注册）——已具备
`get_tile`、`set_tile`、`get_block`、`list_tiles`、`backup`（共 5 个）。
MCP 不可用时，用 execute 工具调用 CLI `world-editer ...`（也可 `python src/world_editer/cli.py ...`）。
如果必须 scripting，直接复用 `src/world_editer/`，不要重新发明 NBT openers。

> `set_block` / `fill` / `diff` / `list_candidates` **尚未实现**，需要时先看 README「已知边界」。

## 快速参考 —— 坐标

- chunk 坐标 `cx = x >> 4`，`cz = z >> 4`；section `sy = y >> 4`
- TileEntity 存在 chunk 的 `TileEntities[]` 列表里，是 NBT Compound
- terrain 方块字节在 `Sections[sy].Blocks[]`（id 0-255）+ `.Data[]` nibble（meta）
- `level.dat` 是全局的（不是 per-chunk）——请明确询问
- 仅 1.12：数据为大端、zlib 压缩（type byte 2），不是 Anvil 格式 1

## NBT 值表示（**别自己判别形态**）

本工具读出的值是异构的：顶层 compound 字段是 `(tag_int, payload)`；list 里的 compound
是**裸 dict**（tag 丢失）；list 元素用字符串 `"list"` / `"intarray"` 冒充 tag；
byte array 是 `(7, ('bytearray', b'...'))` **双层嵌套**。

统一用 `nbt.py` 的访问器，不要在业务代码里写判别：

```python
nb.unwrap(v)        # tagged-value → 朴素值
nb.as_compound(v)   # → dict
nb.as_list(v)       # → list
nb.as_bytes(v)      # → bytes
```

> 这层判别历史上散落 4 处，其中 `block.read_block` 写错导致**恒返回空气**。现在是单点。

## 常见模式

### A. 读取一个命令方块（最安全）

```
get_tile(world, x, y, z)
   -> {coords, chunk, id, Command, CustomName, TrackOutput, LastOutput}
```

### B. Patch 一个命令，别覆盖其它字段

```
set_tile(world, x, y, z, { "Command": "execute ...", "CustomName": "§4foo" })
```

工具合并式 patch，保留 `TrackOutput`、`LastOutput`。**永远 patch，不要覆盖整个 tile**。

### C. 某半径内所有命令方块

```
list_tiles(world, box=(x1,z1,x2,z2), keyword="function")
```

`box` 是 **4 元组**，不是 6 维。`keyword` 只匹配 `Command` 与 `id` 两个字段；
要按其它字段过滤就 `keyword=None` 拿全量再自行筛。

### D. 精确定位 block

```
read_block(world, x, y, z)  -> {id, meta, name}
```

`BLOCKS_1_12` 是 1.12 全表（254 条），由注册表生成。**不要手工增补**。
易错项：`37/38` 是 `yellow_flower`/`red_flower`（顺序与直觉相反）；
`28` 才是 `detector_rail`；`93` 才是中继器（`55` 是红石粉）；
`137/210/211` 才是三种命令方块（210 与 211 极易搞反）。

### E. 动手前备份（always）

```
backup(world)   -> path
```

备份落 `world/backups/<timestamp>/`。用户要回滚 → 恢复文件再 hash 验证。

### F. 批量扫描方块

逐点 `read_block` 会每次重读整个 chunk（O(n²)）。**大批量扫描请用
`block.read_blocks(world, box)`**（每 chunk 只解压一次）。

## 1.12 NBT 陷阱（每次先读）

1. `LastOutput` 是字符串里嵌 JSON，可能尾随 `}`，别 strip
2. NBT 字符串 length-prefixed（short），没有 sentinel
3. Tile ID 是 `minecraft:command_block`（compound id），不是裸 "command_block"
4. NBT integer overflow：yaw/pitch 是弧度 float，不是度
5. `stat.xxx` objective 的值在 NBT 里 **camelCase**，在命令里是 **lowercase/snake**；两边都要匹配拼写
6. NBT keys **大小写敏感** —— `Command` 不是 `command`，`TrackOutput` 不是 `trackoutput`
7. `Sections` 未必每个 y slice 都有（空气 chunk）；decode 前先 check
8. `.Data` 是 byte per block，**不是** nibble per block（unlike `.Light`）
9. 数据存储在 **chunk 里**（region 包含 chunk 的 tile entities），不是 region 文件本身。1 个 .mca = 最多 1024 个 chunk，各自 zlib 压缩。
10. 写入路径**不限定到目标 tile**：patch 作用于整个 chunk，同名字段可能报错或打错对象

## 坐标 quirk

- spawn 永远在 y≈72（地板）；负 y = below bedrock（void）
- `rm`/`r` 范围是 **相对玩家**，单位方块，不是 chunks
- command-block buttons 设置 `auto=0`（默认 redstone-exec）；始终用 `execute`-guarded variants
- chunk 坐标 unsigned（x>>4 对负坐标正常）
- world 与 region 文件是同一世界，但 `region/r.X.Z.mca` 是 chunks/base tiles only；region 文件里没有 top-level `blocks` NBT。

## 别做

- 别 pretty-print NBT：会 break 二进制 diff；diff 解码后的值，不要 diff 文件
- 别把 *.mca 当 UTF-8 读（它是 zlib+binary）
- 别 strip `LastOutput` 的尾部 `"}`"（JSON 尾）
- 别硬编码 region 文件名；用公式
- 别不更新 chunk Time 就写 chunks（flush needed）
- 别忘了本地 gitignore `world/backups/`
- 别把 `stat.xxx` per entity 与 scoreboard 混淆；scoreboard 是独立 NBT storage

## Smoke test 配方

```
1. backup
2. read known button command block
3. modify command + read back (must equal)
4. restore from backup + re-verify
```

这个 skill 配对 MCP 工具 `world-editer`。优先 MCP 而不是 CLI（离线路径更简单）。如果你在 `data/functions/` 改 mcfunction 文本，要知道它和 world 数据是分开的，MCP 工具从不读它——只能经 .mca 改世界。

**测试资源**：`tests/world/` 下有 31 个 .mca fixture（从某世界复制），全部为 1.12 Java，parse_tile_entities 单例 0 error。新增测试时一律用 tests/world 为 world root，避免污染原世界目录。
