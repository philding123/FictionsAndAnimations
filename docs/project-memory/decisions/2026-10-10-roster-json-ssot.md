# 角色设计以 roster.json 为 SSOT，SVG 由脚本确定性生成

- Date: 2026-10-10
- Status: accepted
- Owners: 未记录
- Related issues: [character-sheet-svg-render-defects](2026-10-10-character-sheet-svg-render-defects.md)
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Decision

- 角色外观的唯一事实源是 `characters/roster.json`；`sheet.svg` 由 `tools/gen_character_sheet.py` 确定性生成。改设计 = 改数据 + 重新生成 + 升版本，禁止手改 SVG。

## Context

- 跨集角色一致性是动画化最大的漂移风险，需要可执行（而非靠记忆）的一致性方案。

## Options Considered

- 未记录（决策表仅含结论与理由）。

## Rationale

- "改数据→重生成"杜绝手绘漂移；渲染素材可追溯到 roster.json（全局不变式 R2）。

## Consequences

- Positive: 一致性可机器校验；角色变更历史由 roster 版本承载。
- Negative: 生成器缺陷会成为全局单点（见关联 issue）。
- Follow-up: 未在 roster 定稿的角色不得上屏。

## Verification

- 19 个角色（18 普通 + white-walker）经 3 轮视觉验收迭代通过。
