# 奈德金句按通行译文修复（源文本字节缺损处）

- Date: 2026-10-10
- Status: accepted
- Owners: 未记录
- Related issues: [mobi-source-data-quality](2026-10-10-mobi-source-data-quality.md)
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Decision

- S01E01 中奈德的主题句按通行译文修复为：「人唯有在恐惧之时，方能勇敢。」并在剧本内标注修复事实；源文件缺损处保持留档不动。

## Context

- 源文本该句字节缺损（见 ADR source-quote-fidelity 的省略号默认规则）。

## Options Considered

- 遵循默认规则以省略号标注 —— 被否（仅此句）：台词面向配音与画面，省略号会削弱全剧主题句的力量。

## Rationale

- 默认规则的显式例外：主题句的完整性优先，且修复必须留痕、不回写源文本。

## Consequences

- Positive: 关键台词完整可配音；数据层仍诚实。
- Negative: 形成"默认省略号 + 标注例外"的双轨，需要逐句判断。
- Follow-up: 类似缺损句出现时按同一模式处理（通行译文 + 剧本内标注）。

## Verification

- S01E01 script 中已标注；评审（v0.3）核查通过。
