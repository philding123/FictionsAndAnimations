# episodes/ — 分集制作流水线

> 六阶段门禁定义见根 `PROJECT_SPEC.md` §4；本 README 是操作总览。

## 一季一卷

| 季 | 原著 | 源文件 | 集数规划 |
|----|------|--------|----------|
| season01 | 卷一《权力的游戏》 | `source/text/卷01–卷03`（95 章 / 55.2 万字） | `season01/plan.md`（12 集） |

## 新建一集（标准动作）

```bash
# 1. 复制模板
mkdir -p episodes/season01/S01E09/keyframes
cp episodes/templates/*.md episodes/season01/S01E09/
# 2. 填 plan.md（选材+节拍+角色清单，过门禁①）
# 3. 依次推进 script → storyboard → assets → render → qa
```

## 六阶段与门禁（阶段产物都在该集目录内）

| 阶段 | 文件 | 门禁（不通过不得进入下一阶段） |
|------|------|------|
| ① 选材 | plan.md | 出场角色全部已在 `characters/` 定稿 |
| ② 剧本 | script.md | 2,000–3,500 字；头部元数据含源章节引用 |
| ③ 分镜 | storyboard.md | 镜头表秒数合计 ≤ 600s；55–95 镜 |
| ④ 资产 | assets.md + keyframes/ | 每角色引用 roster.json 调色板与特征 |
| ⑤ 渲染 | render.md | 每段素材时长记录；合成命令可复现 |
| ⑥ 质检 | qa.md | 时长实测 ≤600s；风格与角色一致性对照通过 |

交付：成片 + 字幕复制到 `output/seasonNN/SXXEYY/`，更新 `docs/production-tracker.md`。
视频文件**不得**留在本目录。

## 剧本改编密度（默认值，特殊集需在 plan.md 说明）

- 每集压缩原著约 30:1–60:1；聚焦 2–6 个连续章节的关键场景。
- 名场面保留原文对白（引用格式 `「…」 ——卷NN §章`），过场用旁白压缩。
- 单集叙事线 ≤ 3 条 POV；每集结尾必须有钩子（悬念/危机/反转）。
