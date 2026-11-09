# FictionsAndAnimations · 《冰与火之歌》小说转动画

把《冰与火之歌》（5 卷 15 册）按集改编为**美漫厚涂风格**（参考《双城之战》）的
连续动画短片：一集一条主线，目标 6–10 分钟，按季连续编号（S01E01…）。

> 个人学习 / 研究性质的二次创作。原著版权归乔治 R·R·马丁及出版社所有，
> 产出内容不商用、不公开分发。

## 项目结构

```text
├── PROJECT_SPEC.md      # 制作规范 SSOT（时长/风格/门禁/目录契约）
├── AGENTS.md            # Agent 通用指南（分级地图路由）
├── CLAUDE.md / GEMINI.md
├── MEMORY.md            # 跨会话状态快照（当前进度/下一步/踩坑）
├── source/              # 小说源文本（只读）：15 册 / 365 章纯正文 + 章节索引
├── characters/          # 角色定稿设计：roster.json（SSOT）→ design.md + sheet.svg
├── bible/               # 视觉风格圣经：美漫厚涂可执行定义
├── episodes/            # 分集制作流水线（六阶段门禁）+ season01/ 规划与集产物
├── output/              # 成片输出（唯一视频出口）
├── tools/               # 流水线脚本（提取/拆分/设定图/切割/校验）
└── docs/                # 进度追踪 / 决策记录 / 评审报告
```

## 制作流水线（每集六阶段门禁）

```text
选材 plan → 剧本 script → 分镜 storyboard → 资产 assets → 渲染 render → 质检 qa
```

每阶段有硬门禁（出场角色须定稿、时长 ≤600s 实测、视觉审查通过等），
详见 `PROJECT_SPEC.md` §4。

## 快速开始

```bash
# 从 MOBI 提取小说源文本（15 册 / 365 章纯正文）
python tools/extract_mobi.py "冰与火之歌（套书共15册）.mobi" source/raw/全书_raw.html
python tools/clean_html.py source/raw/全书_raw.html source/raw/全书_clean.txt
python tools/split_books.py

# 重新生成角色设定图（改 characters/roster.json 后）
python tools/gen_character_sheet.py

# 动态分镜 / 成片拼装 / 时长门禁
python tools/build_animatic.py episodes/season01/S01E01
python tools/check_duration.py output/season01/S01E01/S01E01_final.mp4
```

## 当前进度

- 第一季（卷一《权力的游戏》）规划 **18 集**（v2 节奏重构：一集一条线）
- **S01E01《长城之外》**：v2.0 初版成片已交付（360s，4 条图生视频嵌入 + 旁白/环境音）
- 详见 `docs/production-tracker.md` 与 `MEMORY.md`

## 版权与致谢

- 原著：George R·R·Martin《A Song of Ice and Fire》及其中文译者
- 视频生成：可灵 AI（Kling）；关键帧：gpt-image-2
- 本仓库仅含提示词、设定图与工程文件，不含平台生成的成片之外的受版权保护素材
