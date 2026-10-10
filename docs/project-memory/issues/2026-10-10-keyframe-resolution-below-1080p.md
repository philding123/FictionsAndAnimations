# 关键帧分辨率低于 1080p 基准（⑤ 渲染前必须超分）

- Date: 2026-10-10
- Status: open
- Severity: medium
- Owners: 未记录
- Related decisions:
- Related daily notes: [2026-10-10](../daily/2026-10-10.md)

## Symptoms

- S01E01 的 7 张关键帧实际尺寸为宽 1536–1774px（gpt-image-2 经中转端点生成），低于 1920×1080 成片基准。

## Impact

- 若直接进入⑤渲染与图生视频，1080p 成片会放大模糊；交付质量不达标。

## Root Cause

- 生成模型/端点不保证输出 1080p，生成分辨率未在生成前钳制。

## Resolution

- 未解决。计划：⑤ 渲染准备的第一步对全部关键帧统一超分到 1920×1080（超分工具待选型）。

## Validation

- 待超分后逐张核验实际像素尺寸与画面质量（视觉验收复检）。

## Prevention

- 关键帧生成后立即校验尺寸门禁（≥1080p），不达标当场重生成或超分，不留到渲染阶段。
