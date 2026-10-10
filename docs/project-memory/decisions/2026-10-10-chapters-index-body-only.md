# 章节索引只含正文（365 章），过滤跋/附录/家谱

- Date: 2026-10-10
- Status: accepted
- Owners: 未记录
- Related issues: [mobi-source-data-quality](2026-10-10-mobi-source-data-quality.md)
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Decision

- `source/chapters_index.json` 只收录纯正文章节（全书 365 章）；跋/附录/家谱/卷间标记从索引过滤。`tools/split_books.py` 相应加固。

## Context

- 初版索引为 449 章，混入了非正文块；规划若引用虚构章节号，属于数据性硬伤。

## Options Considered

- 未记录（决策表仅含结论与理由）。

## Rationale

- 编号边界必须真实可查：卷一实为 27/26/20 章，规划引用才能落在一等一个真实章节上。

## Consequences

- Positive: 全部 plan 的章节引用可机器校验；索引从 449 修正到 365。
- Negative: 未记录。
- Follow-up: 未记录。

## Verification

- `chapters_index.json` 重建后按卷核对章数（卷一 27/26/20）。
