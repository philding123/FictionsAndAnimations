# characters/ — 角色一致性设计体系

> 规则细节见本目录 `AGENTS.md` 与根 `PROJECT_SPEC.md` §5。本 README 是人读的总览。

## 现有角色（19，第一季班底 + 序幕特效角色）

见自动生成的 [`_index.md`](_index.md)（含定位/首秀集/设计版本）。

## 目录结构

```text
characters/
├── roster.json              # 角色注册表（SSOT：所有外观参数在这里）
├── <character-id>/
│   ├── design.md            # 详细设计（自动区由生成器维护 + 手写叙事区）
│   └── sheet.svg            # 标准设定图（生成物，禁止手改）
└── _index.md                # 自动生成的总索引
```

## 工作流

1. **新增角色**：在 `roster.json` 增加条目（字段结构照抄现有角色）→
   `python tools/gen_character_sheet.py <id>` → 检查生成的 design.md/sheet.svg。
2. **修改设计**：改 roster.json（`design_version` +1）→ 重跑生成器 → 在该角色
   design.md「变更记录」表追加一行 → 重大变更在 `docs/decisions.md` 留痕。
3. **剧集引用**：每集 `assets.md` 列出出场角色 id；渲染 prompt 必须内嵌
   roster.json 的 HEX 调色板 + 标志特征，禁止凭记忆描述外观。

## 设定图内容（sheet.svg，900×1200）

正面像（矢量规范造型）、家族色、调色板 5 色（渲染必引用）、标志特征、
服装描述、气质、底部剪影带（身高/头身标尺 + 道具清单）。

## 预览

`../.preview/<id>.png` 是 Edge 无头渲染的 PNG 预览缓存，可用
`tools/preview_sheets.sh`（待建）或手动 Edge 命令重建；改动 SVG 后请重渲染。
