# 设定图是矢量规范图，厚涂质感在关键帧阶段另行产出

- Date: 2026-10-10
- Status: accepted
- Owners: 未记录
- Related issues:
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Decision

- `sheet.svg` 表达的是"设计规范"（造型/配色/特征清单），不追求最终画面质感；厚涂成品质感由关键帧阶段按 `bible/style-guide.md` §6 执行（AI 生成/人工绘制）。

## Context

- SVG 天然不适合表达厚涂（Arcane 参考）质感，若强求会把规范图做成低劣插画。

## Options Considered

- 未记录（决策表仅含结论与理由）。

## Rationale

- 规范与质感分层后，两层各自有明确的验收标准：规范图看特征/调色板，关键帧看风格圣经。

## Consequences

- Positive: 角色验收关注点清晰；关键帧管线不被 SVG 能力拖累。
- Negative: 关键帧仍需单独保证与规范图的一致性（渲染素材必须引用 roster 调色板 hex）。
- Follow-up: 未记录。

## Verification

- 未记录。
