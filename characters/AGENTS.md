# AGENTS.md — characters/ · 角色定稿设计体系

## 1. 职责与定位

- 解决跨集角色形象漂移：每个角色在这里**一次性定稿**，之后所有剧集只引用、不重设。
- 下游：`episodes/*/assets.md` 必须引用本目录条目；渲染素材必须可追溯。

## 2. 结构与组件

| 文件 | 说明 |
|------|------|
| `roster.json` | **角色注册表（SSOT）**：发/肤/瞳色 hex、体型、年龄感、标志特征、家族色、设计版本号 |
| `<character-id>/design.md` | 详细文字设计：面容、发型、体型、服装（分层）、材质、气质、标志动作/道具、音色气质 |
| `<character-id>/sheet.svg` | 标准设定图（正面像+剪影+调色板+特征标注），由 `tools/gen_character_sheet.py` 从 roster.json 生成 |

character-id 用小写英文连字符（如 `jon-snow`、`daenerys-targaryen`）。

## 3. 铁律与不变式

- 🚫 **禁止手改 `sheet.svg`**（生成物）；🚫 禁止绕过 roster.json 直接给角色改设定。
- **变更流程**：改 `roster.json`（升 `design_version`）→ 必要时同步 `design.md` → 重跑生成器 → 在该角色 design.md 末尾追加变更记录 → 在 `docs/` 决策记录留痕。
- 未定稿角色（本目录无对应条目）**不得上屏**；新增角色先补这里。
- 渲染 prompt 必须内嵌该角色的 palette hex + 特征清单（从 roster.json 取），禁止凭记忆描述。

## 4. 操作

```bash
python tools/gen_character_sheet.py     # roster.json 全量重新生成 sheet.svg
```
- 校验：roster.json 须通过生成器内置 schema 检查（缺字段会报错中止）。
