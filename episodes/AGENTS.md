# AGENTS.md — episodes/ · 分集制作流水线

## 1. 职责与定位

- 每一集的全部**中间产物**（plan/script/storyboard/assets/render/qa）住在这里；
  成片不在这里（→ `output/`）。
- 目录结构：`episodes/season{NN}/S{NN}E{NN}/`，第一季对应原著卷一。

## 2. 结构与组件

```text
episodes/
├── README.md                  # 流水线总说明 + 六阶段模板链接
├── templates/                 # plan/script/storyboard/assets/render/qa 六个模板
└── season01/
    ├── plan.md                # 第一季集数规划（节拍级，SSOT）
    └── S01E01/
        ├── plan.md  script.md  storyboard.md
        ├── assets.md  keyframes/  render.md  qa.md
```

## 3. 铁律与不变式

- 六阶段顺序执行、门禁通过才进下一阶段（门禁定义见 PROJECT_SPEC §4）。
- 🚫 视频文件禁止存放在本目录；🚫 禁止跳过 qa.md 直接交付。
- 每集文件头必须带元数据块：集号、标题、适配源章节、时长目标、出场角色 id 列表。
- 改动剧情节拍先改 `seasonNN/plan.md`，再落到单集文件，保持规划与现实一致。

## 4. 操作

- 新建一集：复制 `templates/` 六个模板到 `seasonNN/SXXEYY/`，逐阶段填充。
- 时长校验：`python tools/check_duration.py output/.../<集号>_final.mp4`（交付门禁）。
