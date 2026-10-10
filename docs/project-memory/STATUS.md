# Project Memory Status

## Snapshot

- Latest daily note: [2026-10-10](./daily/2026-10-10.md)
- [Latest decision](./decisions/2026-10-10-white-walker-fx-character.md)
- [Latest issue](./issues/2026-10-10-mobi-source-data-quality.md)
- Current todo list: [Project Memory TODO](./todo.md)

## Current Focus

## Now

- S01E01 ⑤ 渲染准备：先把 7 张关键帧统一超分到 1920×1080（当前 1536–1774 宽，见 [keyframe-resolution-below-1080p](issues/2026-10-10-keyframe-resolution-below-1080p.md)）。
- 图生视频/动态分镜工具链选型，然后按 `episodes/season01/S01E01/storyboard.md` 79 镜推进渲染，逐段时长记录进 render.md。

## Recent Activity

### Decisions

- [异鬼（white-walker）作为特效角色注册 roster 并走完整定稿流程](./decisions/2026-10-10-white-walker-fx-character.md)
- [完成 S01E01 剧本与全季规划的系统化评审](./decisions/2026-10-10-systematic-review-gate.md)
- [设定图是矢量规范图，厚涂质感在关键帧阶段另行产出](./decisions/2026-10-10-svg-design-spec-not-final-art.md)

### Issues

- [MOBI 提取源文本数据质量（NUL 控制字符 + 字节损坏）](./issues/2026-10-10-mobi-source-data-quality.md)
- [关键帧分辨率低于 1080p 基准（⑤ 渲染前必须超分）](./issues/2026-10-10-keyframe-resolution-below-1080p.md)
- [角色设定图生成器渲染缺陷（重复 font-family + 右栏溢出）](./issues/2026-10-10-character-sheet-svg-render-defects.md)

### Daily Notes

- [2026-10-10](./daily/2026-10-10.md)

## Commands

- `./scripts/project-memory.sh daily`
- `./scripts/project-memory.sh decision <slug>`
- `./scripts/project-memory.sh issue <slug>`
- `./scripts/project-memory.sh note <target> <text>`
- `./scripts/project-memory.sh todo-add <section> <text>`
- `./scripts/project-memory.sh refresh`
- `./scripts/project-memory.sh status`
- `./scripts/validate-project-memory.sh`
