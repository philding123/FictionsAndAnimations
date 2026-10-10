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
- **S01E01《凛冬将至》**：①–④ 完成，⑤ 首里程碑达成。9 张关键帧验收 9/9，HD 归一化
  1920×1080（`keyframes/hd/`），**541.00s 动态分镜过时长门禁**（`seg/S01E01_animatic.mp4`，
  分段表 `seg/segments.json` 是 SSOT，`tools/build_animatic.py` 可复现；mp4 不入库）。
  **当前卡点：成片级图生视频工具链选型**（render.md 列了三条候选路径，涉及 API 成本，需用户拍板）。
- **评审**：`docs/review-s01e01-and-season01-plan.md` 的执行清单已全部整改（v0.4）。
- **图像生成通路**：`OPENAI_API_KEY` 读自 `C:\Users\phil\.codex\auth.json`，
  **必须配 `OPENAI_BASE_URL=https://api.20230112.xyz/v1`**（直连 api.openai.com 会 401）。
- **ffmpeg**：经 `pip install static-ffmpeg` 就位（winget 会挂起，别用）；
  check_duration / build_animatic 已自动发现该路径。

## 下一步（按序）

1. **图生视频（可灵）——阻塞中**：`~/.config/Fiction/env` 的 KLING key 经实证
   **在可灵官方两个端点都不是有效凭证**（api-singapore: "api key not found"；
   api.klingai.com: "Auth failed"；请求头格式已排除问题）。等待用户澄清 key 来源：
   - 若是中转平台 → 还需要 base_url（工具需加 `KLING_BASE` 支持）；
   - 若是官方 → 改为 KLING_AK/KLING_SK 双值（JWT 签名模式已在
     `tools/gen_video_kling.py` 实现，直接可用）。
   工具就绪：`python tools/gen_video_kling.py --image <hd帧> --prompt <运镜描述> --out seg/x.mp4`
2. 音频：对白配音、BGM、音效 → 混入成片（响度 ≈ -16 LUFS）。
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
| 决策留痕 | docs/decisions.md（详版 ADR 在 docs/project-memory/decisions/） |
| 分层项目记忆（ADR/issue/日志/todo） | docs/project-memory/（入口 INDEX.md；`scripts/project-memory.sh` 维护） |
| 评审报告 | docs/review-s01e01-and-season01-plan.md（已整改） |
