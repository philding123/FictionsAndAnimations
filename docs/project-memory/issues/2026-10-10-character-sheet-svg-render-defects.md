# 角色设定图生成器渲染缺陷（重复 font-family + 右栏溢出）

- Date: 2026-10-10
- Status: closed
- Severity: medium
- Owners: 未记录
- Related decisions: [roster-json-ssot](../decisions/2026-10-10-roster-json-ssot.md)
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Symptoms

- 同一 SVG 元素重复 `font-family` 属性 → XML 解析中断，浏览器渲染画面截断。
- 右栏文本换行宽度 >19 个全角字符 → 溢出画布。

## Impact

- `characters/*/sheet.svg` 设定图不可用；角色定稿验收被阻塞（3 轮视觉验收迭代）。

## Root Cause

- `tools/gen_character_sheet.py` 生成器缺陷：属性拼接重复、wrap 宽度上限过大。

## Resolution

- 生成器修复：消除重复属性；右栏 wrap 上限收窄到 16 字符 + 收尾标点。

## Validation

- 19 个角色设定图全部重新生成并通过视觉验收（roster v1）。

## Prevention

- 生成器输出后先做 XML 解析校验再交付预览；改 wrap/属性逻辑后全量重生成回归。
