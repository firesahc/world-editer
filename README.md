# WorldEdit — Minecraft Anvil（.mca）地图数据编辑器工具集

一个**纯标准库、离线运行**的工具集，用于读取和修补 **Minecraft 1.12 Java Edition** 的 Anvil 世界数据。封装成 CLI + MCP，保证你不再需要反复手写临时脚本。

配对知识库：`skill/world-editer.md`（操作流程SOP），在opencode中通过skill工具调用。

## 目录结构

```
world-editer/
├── pyproject.toml
├── README.md
├── src/world_editer/
│   ├── __init__.py
│   ├── nbt.py            # NBT 读写（level / chunk / TileEntity）
│   ├── region.py         # .mca 打开、扇区读写、NBT chunk 修补、备份
│   ├── block.py          # 方块 id/name/1.12 metadata 表格 + Section 修补
│   ├── tile.py           # TileEntity get/put/merge（Command、CustomName）
│   ├── ops.py            # 复合操作：set_block、fill_region、backup、diff
│   └── cli.py            # 无 click 的 argparse CLI：get/set/list/diff/fill
├── mcp/
│   └── server.py         # fastmcp 包装 src/ 函数的 MCP 服务器
├── skill/
│   └── world-editer.md   # 在 opencode 中加载的 SOP skill
└── tests/
    └── smoke.py
```

## 1. nbt.py

```python
def read_nbt(data: bytes) -> (name, root, consumed)
def write_nbt(name, root) -> bytes
def patch_field(raw_nbt, field_name, old_str, new_str) -> bytes
```

手工手写、确定性；针对 1.12 只需要 `TAG_Compound / Tag_List / Tag_String / Tag_Int` 四种。全程保持字节（bytes），避免 utf8 陷阱。

## 2. region.py

```python
def chunk_index(cx, cz) -> (rx, rz, li, sector0)
def read_chunk(world, cx, cz) -> (header, nbt_bytes)
def write_chunk(world, cx, cz, new_nbt) -> dict
    -> {path, old_sector, new_sector, mode: "inplace"/"alloc", backup}
```

扇区分配遵循 edit_cb.py 已验证的模式：`need <= nused` 时原位；否则从文件末尾分配新扇区，更新 `li` 头。除非 world 升级需要，否则不触碰 header 数组中 region/PlayerScores/Teams 绑定。

## 3. block.py

```python
BLOCKS_1_12 = { 57: "minecraft:diamond_block", ... }   # ~300
def decode_block(sections, x, y, z) -> (block_id, meta)    # 1.12 含 Add 位
def encode_block(sections, x, y, z, block_id, meta) -> sections
```

1.12 暂不支持 HMD `Add[]`（bit8），仅 ids<512；BlockMeta 对透明/半透明方块保留原值。

## 4. tile.py

```python
def tile_at(world, x, y, z) -> dict | None
def tile_set(world, x, y, z, patch) -> dict    # patch 为合并式，保留其它字段
def tile_delete(world, x, y, z) -> bool
```

`patch` 示例：`{ "Command": "execute ...", "CustomName": "§4foo" }`，保留 `TrackOutput` 与 `LastOutput`。

## 5. ops.py  (预留)

```python
def backup(world, region_path) -> backup_path
def diff(world, before_nbt, after_nbt) -> patch / counts
def apply_fill(...):   # 区域 fill
```

## 6. cli.py

```text
world-editer get tile  -w <world> -x -y -z
world-editer set tile  -w <world> -x -y -z --json patch.json
world-editer get block -w <world> -x -y -z
world-editer set block -w <world> -x -y -z --id 57 --meta 0
world-editer fill tile|block  [many...]
world-editer list-tiles  -w <world> --keyword "function" --box x1,z1,x2,z2
world-editer diff  before.json after.json
```

## 7. mcp/server.py

用 fastmcp 把 cli 函数包装为 MCP 工具，通过 opencode.jsonc 注册：

```jsonc
"mcp": {
  "world-editer": {
    "type": "local",
    "command": ["C:\\path\\python.exe", "mcp/server.py", "-w", "<world>"],
    "enabled": true
  }
}
```

## 8. skill/world-editer.md

SOP + 常见模式示例：
- “坐标尚未生成时：world.put_chunk(...)” (raise, 不崩溃)
- fastmcp 读 nbt 的陷阱（utf8、lastoutput）
- backup 命名 + 宏
- 1.12 坐标映射数学

## 构建 / 安装

```bash
cd "D:\D\User Data\Documents\vscode Projects\world-editer"
python -m venv .venv
pip install fastmcp>=3.0.2 pytest   # 可选，仅 mcp 测试
pip install -e .                    # 安装为 package
```

## 测试

`tests/smoke.py` 检查：
- 读取已生成 chunk
- 写入 tile + 读回
- idempotency of set block

## 说明

- 仅 1.12；数据为大端 NBT + zlib
- lastoutput 在 diff 中被保留；不要 strip
- 若 changed tile entity 在 chunk 中不存在，不要自动创建（本 map 是静态布局，按钮/压敏/button 压敏部位）
- parser 应为 **字节字面量**（而非 JSON pretty I/O）。在控制台解码请 `.decode('utf-8')`
- windows git path 存在空格：请引用

## 待开发 checklist

- [ ] nbt.py read/write
- [x] region read/write with backup + sector alloc
- [x] block + tile modules（tile parse 已通）
- [ ] cli
- [ ] mcp server
- [ ] skill SOP
- [ ] run tests on world before release
- [ ] register opencode mcp entry
- [x] backups 目录本地 gitignore
- [ ] tile.set / block.write_block
- [ ] 集成 smoke 填充 region round-trip
