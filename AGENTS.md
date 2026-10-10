# AGENTS.md — 《冰与火之歌》动画化项目 · 通用 Agent 指南（SSOT）

## 1. 工程背景

本目录是一个**小说转连续动画**的制作项目（非传统代码仓库）：
把《冰与火之歌》全书（5 卷 15 册，源文本在 `source/`）按集改编为每集 ≤10 分钟的
美漫厚涂风格（参考《双城之战》）动画片。所有制作规则见 `PROJECT_SPEC.md`（规范 SSOT）。

## 2. 目录契约（端口契约等价物：目录即接口）

| 目录 | 角色 | 写权限 |
|------|------|--------|
| `source/` | 小说源文本 + 章节索引（只读输入） | 🚫 禁止修改 |
| `characters/` | 角色定稿设计（design.md + sheet.svg + roster.json） | 仅通过 roster.json/design.md 变更再重新生成 |
| `bible/` | 风格圣经（style-guide.md，视觉唯一依据） | 变更须全项目生效，谨慎 |
| `episodes/` | 每集全部中间产物（plan/script/storyboard/assets/render/qa） | 按集目录写入 |
| `output/` | 成片输出（唯一视频出口） | 仅 `_final.mp4` + `.srt` |
| `tools/` | 流水线脚本（提取/拆分/设定图生成/时长校验） | 可加新工具，勿破坏既有命令 |
| `docs/` | 进度追踪、决策记录 | 随做随更新 |

## 3. 全局不变式（Fail-Closed，违反即返工）

1. **时长红线**：任何成片 > 600.0s 一律不得交付（`python tools/check_duration.py <mp4>`）。
2. **角色一致性**：未在 `characters/` 定稿的角色不得上屏；渲染素材必须能追溯到 roster.json。
3. **source 只读**：源文本任何"顺手修正"都是破坏；引用时写 `卷NN_标题_X §章节号`。
4. **视频不出双门**：`episodes/` 无成片、`output/` 无工程文件。
5. **SVG 不手改**：`sheet.svg` 是生成物，改设计先改 roster.json/design.md。
6. **命名协议**：集号 `S{SS}E{EE}`；无编号的媒体文件禁止入库。

## 4. Agent 调查预算（渐进式阅读）

- 进入任何子目录前，先读根目录路由表定位，再读该子目录的 `AGENTS.md`（≤60 行）。
- 超过 200 行的文本（如 `source/text/*.txt` 单册 18–26 万字）**必须切片读取**，
  优先使用 `source/chapters_index.json` 定位章节，禁止通读。
- 复杂制作任务先产出提纲（plan.md）并对照 PROJECT_SPEC.md 第 4 节门禁，再动手。

## 5. 分级地图索引（子模块路由表）

| 子模块 | 定位 | 指南入口 |
|--------|------|----------|
| `source/` | 只读小说源文本与索引 | [source/AGENTS.md](source/AGENTS.md) |
| `bible/` | 视觉风格圣经 | [bible/AGENTS.md](bible/AGENTS.md) |
| `characters/` | 角色定稿设计体系 | [characters/AGENTS.md](characters/AGENTS.md) |
| `episodes/` | 分集制作流水线 | [episodes/AGENTS.md](episodes/AGENTS.md) |
| `output/` | 成片输出契约 | [output/AGENTS.md](output/AGENTS.md) |
| `tools/` | 制作工具链 | [tools/AGENTS.md](tools/AGENTS.md) |
| `docs/` | 进度与决策（无子指南，见本文件） | — |

## 6. 常用命令

```bash
# 重新从 MOBI 提取源文本（仅当 source/ 缺失或损坏）
python tools/extract_mobi.py "冰与火之歌（套书共15册）.mobi" source/raw/全书_raw.html
python tools/clean_html.py source/raw/全书_raw.html source/raw/全书_clean.txt
python tools/split_books.py

# 重新生成全部角色设定图（改 roster.json 后）
python tools/gen_character_sheet.py

# 成片时长门禁（交付前必跑）
python tools/check_duration.py output/season01/S01E01/S01E01_final.mp4
```
