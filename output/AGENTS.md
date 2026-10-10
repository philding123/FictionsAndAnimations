# AGENTS.md — output/ · 成片输出契约

## 1. 职责与定位

- 全项目**唯一的视频出口**。交付物按季/集归档，可直接对外播放。

## 2. 结构与组件（契约）

```text
output/season{NN}/S{NN}E{EE}/
├── S{NN}E{EE}_final.mp4   # 成片：1920×1080、24fps、H.264、时长 ≤ 600s
└── S{NN}E{EE}.srt         # 外挂中文字幕（与成片同名）
```

## 3. 铁律与不变式

- 🚫 禁止存放工程文件、图片素材、剧本、关键帧（它们属于 `episodes/`）。
- 成片命名必须 `S{NN}E{EE}_final.mp4`；重修版覆盖同名文件，版本记录写在该集 `qa.md`。
- 交付前必须通过：`python tools/check_duration.py <mp4>`（>600s 拒收）。

## 4. 操作

- 交付 = 复制成片入位 + 更新 `docs/production-tracker.md` 状态为「已交付」。
