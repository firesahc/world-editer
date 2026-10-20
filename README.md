# WorldEdit — Minecraft Anvil（.mca）地图数据编辑器工具集

一个**纯标准库、离线运行**的工具集，用于读取和修补 **Minecraft 1.12 Java Edition** 的 Anvil 世界数据。封装成 CLI + MCP，保证你不再需要反复手写临时脚本。

配对知识库：`skill/world-editer.md`（操作流程SOP），在opencode中通过skill工具调用。

> 本文档描述的是**实际存在的**接口。未实现的能力不会在这里出现。
> 需要尚未实现的能力时，先看「已知边界」一节。

## 目录结构

```
world-editer/
├── pyproject.toml
├── README.md
├── src/world_editer/
│   ├── __init__.py
│   ├── nbt.py            # NBT 读写 + 值表示的唯一访问入口
│   ├── region.py         # .mca 打开、扇区读写、chunk 修补、备份、文件差异
│   ├── chunk.py          # chunk 读写视图：方块/tile 定位、批量遍历、语义差异
│   ├── block.py          # 1.12 方块语义：id↔名字全表、读写门面、批量填充
│   ├── tile.py           # TileEntity 查询/合并式修改（Command、CustomName）
│   └── cli.py            # argparse CLI：get/set/list/fill/diff/backup
├── mcp/
│   └── server.py         # fastmcp 包装 src/ 函数的 MCP 服务器
├── skill/
│   └── world-editer.md   # 在 opencode 中加载的 SOP skill
└── tests/
    └── smoke.py
```

依赖方向是单向的：`cli / mcp → tile / block → chunk → region → nbt`，没有回指。

## 1. nbt.py —— NBT 编解码 + 值表示的唯一入口

```python
def read_root(data: bytes) -> (name, root_dict, consumed)
def write_root(name, comp) -> bytes
def patch_field(raw_nbt, field_name, old_str, new_str) -> bytes
def patch_int(raw_nbt, field_name, new_int) -> bytes
def walk(comp, path="")            # 遍历叶子
def find_field_path(comp, target)  # 按字段名找路径
```

### 值表示的访问器（重要）

本模块读出的值是**异构**的：

| 位置 | 形态 |
|---|---|
| 顶层 compound 字段 | `(tag_int, payload)` |
| list 里的 compound 元素 | **裸 dict**（tag 丢失） |
| list 里的 list 元素 | `("list", sub_tag, [...])`（用字符串冒充 tag） |
| list 里的数组元素 | `("intarray" / "longarray", [...])` |
| byte array | `(7, ('bytearray', b'...'))` —— **双层嵌套** |

因此**不要在业务代码里自己判别形态**。统一用这四个函数：

```python
def unwrap(v)          # tagged-value → 朴素 Python 值
def as_compound(v)     # → dict（兼容裸 dict 与 (TAG_COMPOUND, dict)）
def as_list(v)         # → list
def as_bytes(v)        # → bytes（兼容双层 byte array）
```

> 历史上这块判别逻辑曾散落在 4 个模块里，其中 `block.read_block` 写错导致**恒返回空气**。
> 现在它是单点。

## 2. region.py —— region 文件与扇区 IO

```python
def chunk_location(world, cx, cz) -> (rf, li, sector, raw)
def read_chunk(world, cx, cz) -> (data, rf, li, sector, start, ln, raw)
def write_chunk(world, cx, cz, new_nbt_bytes) -> dict
    # -> {path, mode: "inplace"/"alloc", old_sectors, new_sectors}
def backup_region(world, region_path) -> Path
def decompress_chunk_payload(raw, start, nsec, ln) -> bytes
def parse_tile_entities(data) -> list[dict]
```

扇区分配遵循已验证的模式：`need <= nsec` 时原位写；否则从文件末尾分配新扇区并更新 `li` 头。除非 world 升级需要，否则不触碰 header 数组中 region/PlayerScores/Teams 绑定。

`decompress_chunk_payload` 对**短报长度或损坏**的 payload 有多路回退（完整扇区区 → 声明区 → `decompressobj`），比较稳。

`parse_tile_entities` 返回的每个 dict 的值都已 `unwrap` 过，是朴素 Python 值。

## 3. block.py —— 1.12 方块语义

```python
BLOCKS_1_12 = {0: "air", 1: "stone", ...}   # 254 条，完整
def block_name(bid) -> str                   # 未知 id 返回 "unknown_<id>"
def read_block(world, x, y, z) -> dict       # {"id":…, "meta":…, "name":…}
```

`BLOCKS_1_12` 由官方注册表快照生成：

```
https://github.com/PrismarineJS/minecraft-data  ->  data/pc/1.12/blocks.json
```

**不要手工增补这张表**——极易把 id 与名字对应错。几个容易记错的：

| id | 名字 | 说明 |
|---:|---|---|
| 37 / 38 | `yellow_flower` / `red_flower` | 顺序与直觉相反 |
| 28 | `detector_rail` | 不是 158 |
| 93 / 94 | `unpowered_repeater` / `powered_repeater` | 不是 55（55 是 `redstone_wire`） |
| 137 / 210 / 211 | `command_block` / `repeating_command_block` / `chain_command_block` | 210 与 211 极易搞反 |
| 149 / 150 | `unpowered_comparator` / `powered_comparator` | |

1.12 暂不支持 HMD `Add[]`（bit8），仅 ids<512。

## 4. tile.py —— TileEntity 查询与修改

```python
def tile_at(world, x, y, z) -> dict | None
def tile_set(world, x, y, z, patch) -> dict   # 合并式 patch
def tile_list(world, box=None, keyword=None) -> list[dict]
def tile_delete(world, x, y, z)                # 1.12 未实现，抛 NotImplementedError
```

`patch` 示例：`{ "Command": "execute ...", "CustomName": "§4foo" }`，保留 `TrackOutput` 与 `LastOutput`。

`box` 是 **4 元组** `(x1, z1, x2, z2)`，不是 6 维。

`keyword` 只匹配 `Command` 与 `id` 两个字段。

## 5. cli.py

```text
world-editer get tile  -w <world> --x <x> --y <y> --z <z>
world-editer get block -w <world> --x <x> --y <y> --z <z>
world-editer set tile  -w <world> --x <x> --y <y> --z <z> --json patch.json
world-editer list      -w <world> [--keyword KW] [--box x1,z1,x2,z2]
world-editer backup    -w <world> [--label L]
```

也可以直接 `python src/world_editer/cli.py ...` 运行。

## 6. mcp/server.py

用 fastmcp 把 `src/` 的函数包装为 MCP 工具，通过 opencode.jsonc 注册：

```jsonc
"mcp": {
  "world-editer": {
    "type": "local",
    "command": ["C:\\path\\python.exe", "mcp/server.py", "-w", "<world>"],
    "enabled": true
  }
}
```

**实际暴露的工具**（共 5 个）：

| 工具 | 签名 |
|---|---|
| `get_tile` | `(x, y, z) -> dict` |
| `set_tile` | `(x, y, z, patch_json) -> dict` |
| `get_block` | `(x, y, z) -> dict` |
| `list_tiles` | `(keyword, x1, z1, x2, z2) -> list` |
| `backup` | `(label) -> str` |

## 7. skill/world-editer.md

SOP + 常见模式示例：坐标换算、fastmcp 读 nbt 的陷阱、backup 命名、1.12 坐标映射数学。

## 构建 / 安装

```bash
cd "D:\D\User Data\Documents\vscode Projects\world-editer"
python -m venv .venv
pip install fastmcp>=3.0.2   # 可选，仅 mcp
pip install -e .              # 安装为 package，提供 world-editer 命令
```

## 测试

```bash
python tests/smoke.py
```

`tests/smoke.py` 检查：
- 全部 `.mca` 文件逐 chunk 解析，0 错误
- 读出一个命令方块 tile
- `tile_list` 可用
- **`read_block` 在已知命令方块坐标上返回真实 id**（不是空气）

## 已知边界

以下能力**尚未实现**，需要时再按真实需求设计，不要预设：

- `tile_delete`（1.12 删 tile entity 非平凡）
- `fill`（区域方块批量写入）
- `diff`（两次状态比对）
- 1.13+ 的 `BlockStates` / palette 格式
- 写入路径**不限定到目标 tile**：`patch_field` / `patch_int` 作用于整个 chunk，
  同一 chunk 内存在同名字段时可能报错或打到别的对象。**改图前务必先备份并逐条验证。**
- `write_chunk` 不更新 chunk 的 `LastUpdate` 时间戳

## 说明

- 仅 1.12；数据为大端 NBT + zlib
- `LastOutput` 是字符串里嵌 JSON，可能尾随 `"}`，别 strip
- NBT keys **大小写敏感** —— `Command` 不是 `command`
- 若目标 tile entity 在 chunk 中不存在，不要自动创建
- parser 应为 **字节字面量**（而非 JSON pretty I/O）。在控制台解码请 `.decode('utf-8')`
- Windows 控制台默认 GBK：打印中文会 `UnicodeEncodeError`，请写 UTF-8 文件再读
- windows git path 存在空格：请引用

## 待开发 checklist

- [x] nbt.py read/write + 统一值访问器
- [x] region read/write with backup + sector alloc
- [x] block 全表（254 条，由注册表生成）+ 单点读取
- [x] tile 查询 / 合并式修改 / 列表
- [x] cli（get tile / get block / set tile / list / backup）
- [x] mcp server（5 个工具）
- [x] skill SOP
- [x] smoke test 覆盖全部 fixture
- [x] backups 目录本地 gitignore
- [x] 写入路径限定到目标 tile
- [x] 批量方块读取 API（消除逐点读 chunk 的 O(n²)）
- [x] region 文件 raw 缓存
- [ ] set block / fill / diff（按真实需求再定）
