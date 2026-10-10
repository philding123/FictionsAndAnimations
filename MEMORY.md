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

1. **图生视频——桌面端通路已全线验证 ✅**：可灵桌面 App + pyautogui 桌面自动化，
   试点（kf-011）实测 **60 灵感值/5s 条**，~2 分钟/条，出片 1080p24 与项目标准一致，
   产物 `seg/kling_pilot_kf-011.mp4`。余额 356（≈5 条）。
   - **待用户决策**：批量策略（全量 79 镜=4,740 灵感值 / 重点镜头 12-16 个=720-960 / 场景级 9 个=540）
   - 运行桌面自动化期间用户不能动鼠标键盘（会抢焦点）
2. 音频：对白配音、BGM、音效 → 混入成片（响度 ≈ -16 LUFS）。
3. 质检交付：`check_duration.py` 门禁 → 成片入 `output/season01/S01E01/`。
4. E02 启动前：定稿批次一角色 8 人（名单在 season01/plan.md 末尾）。

## 踩过的坑（别再踩）

- MOBI 提取的文本含 NUL 控制字符 → 会导致部分工具判定为二进制（已在 clean_html.py 过滤）。
- 源文本有字节损坏（如布兰Ⅰ"方能勇敢"句）→ 引用时按通行译文修复并在剧本内标注。
- Git Bash 里 `"...\\$var"` 会转义成字面 `\$var` → Windows 路径一律用正斜杠。
- SVG 中同一元素重复 `font-family` 属性 → XML 解析中断，浏览器渲染截断（生成器已修复）。
- 右栏文本换行宽度 >19 个全角字符会溢出画布（生成器 wrap 上限 16+收尾标点）。
- **桌面自动化坐标**：Read 工具显示的截图是缩放过的，点击坐标必须按 ImageGrab 原始像素（2560×1600）换算；
  坐标系一乱就先全屏截图裁块放大重定位。
- **桌面自动化期间用户不能动鼠标键盘**：焦点被抢会把键入送进错误窗口（发生过：文件路径敲进了前台浏览器）。
  每个操作批次控制在 15 秒内，批次间留用户操作空隙。
- 可灵网页/桌面端上传控件在自动化注入（DataTransfer/paste）下会报"Network error"——
  **桌面 App + 原生文件对话框（pyautogui 输路径）是唯一稳定上传通路**。

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
