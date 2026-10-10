# 单集客串角色也走 roster 定稿流程

- Date: 2026-10-10
- Status: accepted
- Owners: 未记录
- Related issues:
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Decision

- 只出场一次的客串角色（如序幕三人组）同样必须在 `characters/` 走完整定稿流程（design.md + sheet.svg + roster.json 注册）后才可上屏。

## Context

- 一致性规则若给"背景角色"开例外，例外会成为漂移入口。

## Options Considered

- 未记录（决策表仅含结论与理由）。

## Rationale

- R4（角色门禁）不设例外；怪物/特效角色同理（见 ADR white-walker-fx-character）。

## Consequences

- Positive: 渲染素材 100% 可追溯到 roster.json。
- Negative: 客串角色的制作成本固定存在。
- Follow-up: 待补角色按三批排期（名单在 `episodes/season01/plan.md` 末尾）。

## Verification

- 未记录。
