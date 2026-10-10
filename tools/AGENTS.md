# AGENTS.md — tools/ · 制作工具链

## 1. 职责与定位

- 无外部重型依赖的 Python 流水线脚本：源文本提取、分册、角色设定图生成、时长校验。
- 原则：标准库优先；每个脚本可独立运行，`--help`/docstring 可用。

## 2. 结构与组件

| 脚本 | 说明 |
|------|------|
| `extract_mobi.py` | MOBI(PalmDOC/UTF-8) → 原始 HTML 文本 |
| `clean_html.py` | 剥离标签 → 纯文本（保留分页符） |
| `split_books.py` | 清洗文本 → 15 分册 + `source/chapters_index.json` |
| `gen_character_sheet.py` | `characters/roster.json` → 每角色 `sheet.svg`（确定性生成） |
| `check_duration.py` | mp4 时长门禁（>600s 非零退出） |

## 3. 铁律与不变式

- 脚本只写自己的明确输出路径，禁止顺手写其他目录。
- `gen_character_sheet.py` 的输出必须**确定性**（同 roster → 同 SVG），保证可复现。
- 破坏性重建（如重跑 `split_books.py`）前先确认输出目录可覆盖。

## 4. 操作

- 全部命令见根 `AGENTS.md` §6；新增工具须同步该表与下表。
