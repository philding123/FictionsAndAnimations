# 项目记忆（MEMORY.md）— 跨会话状态快照

> 新会话/新 Agent 先读这里再动手：**当前在哪、下一步干什么、别踩哪些坑**。
> 规则类内容不在此重复（见 PROJECT_SPEC.md 与各目录 AGENTS.md）；本文件只记"活的状态"。
> 每次阶段性收尾时更新本文件。

## 项目是什么（一句话）

把《冰与火之歌》全 5 卷改编为每集 ≤10 分钟的美漫厚涂（Arcane 风格参考）连续动画。
规则 SSOT：`PROJECT_SPEC.md`；视觉 SSOT：`bible/style-guide.md`；角色 SSOT：`characters/roster.json`。

## 当前状态（2026-10-10）

- **数据层**：源文本 15 册 / **365 章纯正文**已入库（`source/text/` + `chapters_index.json`，
  跋/附录/家谱已过滤；卷一 = 上27/中26/下20 章）。原 MOBI 提取管线在 `tools/`。
- **角色层**：19 个角色定稿（18 普通角色 + white-walker 特效角色），全部过视觉验收。
  改设计 = 改 roster.json → `python tools/gen_character_sheet.py` → 升版本。
- **第一季**：12 集规划定稿（含评审后的 E10–E12 季终重排：E11 奈德之死、E12 称王+孵龙）。
- **S01E01《凛冬将至》**：①选材 ✅ ②剧本 ✅ ③分镜 ✅（79 镜/541s）④资产清单 ✅。
  **当前进行到：④→⑤ 之间——关键帧生成。**
- **评审**：`docs/review-s01e01-and-season01-plan.md` 的执行清单已全部整改（v0.2）。

## 下一步（按序）

1. **生成 S01E01 的 7 张关键帧**：prompt 批次已就绪
   （`episodes/season01/S01E01/keyframes/prompts.jsonl`，命令见 assets.md）。
   ⚠️ **阻塞：环境未设置 `OPENAI_API_KEY`**（内置图像工具不可用，imagegen 技能 CLI 是唯一路径，
   openai 包已装好）。密钥就绪后跑一条 generate-batch 命令 → 视觉验收 → 更新 assets.md。
2. 渲染合成（需要图生视频/动态分镜工具链 + ffmpeg），`render.md` 记录逐段时长。
3. 质检交付：`check_duration.py` 门禁 → 成片入 `output/season01/S01E01/`。
4. E02 启动前：定稿批次一角色 8 人（名单在 season01/plan.md 末尾）。

## 踩过的坑（别再踩）

- MOBI 提取的文本含 NUL 控制字符 → 会导致部分工具判定为二进制（已在 clean_html.py 过滤）。
- 源文本有字节损坏（如布兰Ⅰ"方能勇敢"句）→ 引用时按通行译文修复并在剧本内标注。
- Git Bash 里 `"...\\$var"` 会转义成字面 `\$var` → Windows 路径一律用正斜杠。
- SVG 中同一元素重复 `font-family` 属性 → XML 解析中断，浏览器渲染截断（生成器已修复）。
- 右栏文本换行宽度 >19 个全角字符会溢出画布（生成器 wrap 上限 16+收尾标点）。

## 关键路径速查

| 要什么 | 去哪 |
|--------|------|
| 每集制作流程/门禁 | PROJECT_SPEC.md §4 + episodes/README.md |
| 角色外观/调色板 | characters/roster.json（渲染必引用） |
| 设定图预览 PNG | .preview/（缓存，可删，Edge 无头重渲染） |
| 章节定位 | source/chapters_index.json |
| 进度唯一事实源 | docs/production-tracker.md |
| 决策留痕 | docs/decisions.md |
| 评审报告 | docs/review-s01e01-and-season01-plan.md（已整改） |
