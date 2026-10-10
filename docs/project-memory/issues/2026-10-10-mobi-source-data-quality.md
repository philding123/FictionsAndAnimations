# MOBI 提取源文本数据质量（NUL 控制字符 + 字节损坏）

- Date: 2026-10-10
- Status: closed
- Severity: high
- Owners: 未记录
- Related decisions: [source-quote-fidelity](../decisions/2026-10-10-source-quote-fidelity.md), [chapters-index-body-only](../decisions/2026-10-10-chapters-index-body-only.md)
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Symptoms

- 提取出的文本含 NUL 控制字符，部分工具把文件判定为二进制拒绝处理。
- 个别句子字节损坏（如卷一布兰Ⅰ"方能勇敢"句缺字）。

## Impact

- `source/text/` 15 册 / 全部下游工具与章节索引不可用或不可信。

## Root Cause

- MOBI 提取管线（extract_mobi.py / clean_html.py）未过滤控制字符；字节损坏为源文件固有。

## Resolution

- `clean_html.py` 增加 NUL 控制字符过滤。
- 字节损坏句：源文件保持只读留档；剧本引用处按通行译文修复并显式标注（见 ADR ned-quote-restore）。

## Validation

- 重建后 `chapters_index.json` 收录 365 章纯正文，工具链全部可读；卷一核对为 27/26/20 章。

## Prevention

- 提取管线对控制字符做默认过滤；引用源文本时先校验字节完整性。
