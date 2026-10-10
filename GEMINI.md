# GEMINI.md — 《冰与火之歌》动画化项目 · 架构定位与分级地图

## 架构全貌

```text
source/（只读小说文本）──选材──▶ episodes/SXXEYY/（六阶段流水线）
                                     │  ▲ 角色引用（roster.json 定稿，禁止即兴）
                                     ▼  │
bible/style-guide.md（视觉唯一依据）─▶ 资产与渲染 ──成片──▶ output/seasonXX/
                                     ▲
tools/（提取/拆分/设定图生成/时长校验）
```

- **定位**：创意生产流水线，不是软件仓库。质量靠规范 + 门禁而非测试套件。
- **协同规则**：任何模块不得越目录写文件（契约见根 `AGENTS.md` §2）。

## 常用命令

```bash
python tools/gen_character_sheet.py    # roster.json → characters/*/sheet.svg
python tools/check_duration.py <mp4>   # ≤600s 门禁（R1）
```

## 铁律与红线（详见 PROJECT_SPEC.md §2）

1. 每集 ≤ 10 分钟；按集编号 SXXEYY；禁止整卷超长视频。
2. 美漫厚涂风格（Arcane 参考），视觉以 `bible/style-guide.md` 为唯一依据。
3. 角色一致：无 `characters/` 定稿不上屏；SVG 为生成物禁手改。
4. `source/` 只读；`output/` 只进成片与字幕。

## 分级地图索引

- [source/AGENTS.md](source/AGENTS.md) — 只读源文本与章节索引（15 册 / 365 章纯正文）
- [bible/AGENTS.md](bible/AGENTS.md) — 风格圣经
- [characters/AGENTS.md](characters/AGENTS.md) — 角色定稿体系
- [episodes/AGENTS.md](episodes/AGENTS.md) — 分集流水线（六阶段门禁）
- [output/AGENTS.md](output/AGENTS.md) — 成片输出契约
- [tools/AGENTS.md](tools/AGENTS.md) — 工具链
- [docs/](docs/) — 进度追踪（production-tracker.md）
