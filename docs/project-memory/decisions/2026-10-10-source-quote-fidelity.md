# 源文本引用保留译文原句，字节损坏处以省略号标注

- Date: 2026-10-10
- Status: accepted
- Owners: 未记录
- Related issues: [mobi-source-data-quality](2026-10-10-mobi-source-data-quality.md)
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Decision

- 剧本引用源文本时保留译文原句；源文件字节损坏处默认以省略号标注，不做静默改写。个别面向配音/画面的主题句可按通行译文修复（须在剧本内标注，如 S01E01 奈德金句，见 ADR ned-quote-restore）。

## Context

- 源文本存在字节损坏（如布兰Ⅰ"方能勇敢"句）；全局不变式 R7 要求引用可回溯（`卷NN_标题_X §章节号`）。

## Options Considered

- 未记录（决策表仅含结论与理由）。

## Rationale

- 可回溯 + 诚实标注数据质量；修复权留在剧本层并留痕，不污染只读源文本。

## Consequences

- Positive: 数据层保持只读与可审计；损坏有据可查。
- Negative: 个别台词需人工复核通行译文。
- Follow-up: 见 ADR ned-quote-restore 的例外规则。

## Verification

- 未记录。
