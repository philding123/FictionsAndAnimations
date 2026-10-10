# CLAUDE.md — 《冰与火之歌》动画化项目

@AGENTS.md

## 项目一句话

把《冰与火之歌》（源文本 `source/`，只读）按集改编为每集 ≤10 分钟的美漫厚涂
（Arcane 风格参考）连续动画。制作规则 SSOT：`PROJECT_SPEC.md`。

## 常用命令

```bash
python tools/gen_character_sheet.py                          # 生成角色设定图
python tools/check_duration.py output/season01/S01E01/S01E01_final.mp4   # 时长门禁
python tools/split_books.py                                  # 重建源文本分册（一般勿跑）
```

## 🚫 绝对禁止（YOU MUST NOT）

- ❌ 修改 `source/` 下任何文件（源文本只读）
- ❌ 产出 > 600 秒的"成片"或绕过时长门禁交付
- ❌ 让未定稿角色（`characters/` 无 design.md + sheet.svg）上屏
- ❌ 把视频放进 `episodes/`、把工程文件放进 `output/`
- ❌ 手改 `characters/*/sheet.svg`（生成物；改 roster.json 后重新生成）
- ❌ 一次性把整卷做成超长视频（本项目按集制作）

## ⚠️ 强约束（IMPORTANT）

- 每集开工前必读：`PROJECT_SPEC.md` → 该集所在 `episodes/seasonXX/plan.md` → `episodes/AGENTS.md`
- 每集六阶段门禁（选材→剧本→分镜→资产→渲染→质检）按序通过，见 PROJECT_SPEC 第 4 节
- 出场角色渲染必须引用 `characters/roster.json` 的调色板 hex 与特征清单

## 子模块路由表（进入子目录前先读对应指南）

| 路径 | 职责 |
|------|------|
| [MEMORY.md](MEMORY.md) | **跨会话状态快照：先读这个**（当前进度/下一步/踩坑） |
| [source/AGENTS.md](source/AGENTS.md) | 只读源文本（15 册 / 365 章）与章节索引 |
| [bible/AGENTS.md](bible/AGENTS.md) | 视觉风格圣经（美漫厚涂规范） |
| [characters/AGENTS.md](characters/AGENTS.md) | 角色一致性体系（roster + 设计图） |
| [episodes/AGENTS.md](episodes/AGENTS.md) | 分集制作流水线与六阶段门禁 |
| [output/AGENTS.md](output/AGENTS.md) | 成片输出契约（唯一视频出口） |
| [tools/AGENTS.md](tools/AGENTS.md) | 工具链（提取/拆分/设定图/校验） |
| [docs/](docs/) | 进度追踪与决策记录（无子指南） |
