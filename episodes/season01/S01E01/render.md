# S01E01 渲染与合成（render.md）

> 门禁⑤：每段素材时长记录在案；合成命令可复现（改参数必须回填本文件）。

## 素材段清单

**动态分镜（animatic，2026-10-10 完成首个可测版本）**：
9 段 Ken Burns 运镜（HD 关键帧 + zoompan），分段表 `seg/segments.json`（SSOT），
构建命令可复现：

```bash
python tools/build_animatic.py episodes/season01/S01E01
python tools/check_duration.py episodes/season01/S01E01/seg/S01E01_animatic.mp4
# [PASS] 541.00s / 上限 600s（H.264 1920×1080 24fps，crf18，约 198MB 中间产物，不入库）
```

| 段 | 关键帧 | 时长(s) | 运镜 | 覆盖镜号 | 场景 |
|----|--------|---------|------|----------|------|
| seg01 | kf-001 | 49 | push-in | 001–010 | S1 鬼影森林 |
| seg02 | kf-011 | 52 | pan-right | 011–020 | S1–S2 异鬼现身与扼杀 |
| seg03 | kf-024 | 79 | slow-push | 021–032 | S3 刑场宣判 |
| seg04 | kf-039 | 56 | pull-out | 033–040A | S4 母狼与六只幼崽 |
| seg05 | kf-043 | 37 | push-in | 041–046 | S5 潘托斯欺压 |
| seg06 | kf-048 | 61 | pan-left | 047–054A | S6 卡奥寝宫初见 |
| seg07 | kf-055 | 35 | push-in | 055–059 | S7 国王驾到 |
| seg08 | kf-060 | 80 | slow-push | 060–065 | S8 墓窖对话与任命 |
| seg09 | kf-073 | 92 | pull-out | 066–075 | S9 塔顶偷听与坠落+片尾 |
| | **合计** | **541** | | | 与 storyboard.md 一致 ✅ |

## 后续：图生视频（真正渲染，待工具链选型）

动态分镜验证了时长与节奏；成片级渲染需要图生视频工具链把每镜关键帧变成运动镜头。
候选路径（**需用户决策，涉及 API 成本**）：

1. 当前中转端点（api.20230112.xyz）若代理视频模型（sora-2 / veo 等）→ 沿用现有密钥；
2. 可灵/即梦等国内视频生成 API（需另开密钥）；
3. 本地 ComfyUI + 开源图生视频模型（需 GPU 资源）。

每镜成片段落生成后按上表逐段登记实际时长，超支按 storyboard.md 的收缩预案执行。

## 合成

- 分辨率/帧率/编码：1920×1080 / 24fps / H.264（PROJECT_SPEC §6）
- 音轨：配音 / BGM / 音效；响度 ≈ -16 LUFS（animatic 暂为无声，配音在剧本对白锁定后录制）
- 合成命令（实际执行版本，含 filter 参数）：见 `tools/build_animatic.py`
  （zoompan 预放大 3840px 抑制抖动，逐段 libx264 crf18，concat demuxer 无损拼接）

## 校验

```bash
python tools/check_duration.py output/season01/S01E01/S01E01_final.mp4
```

- animatic 实测时长：**541.00s ✅**（2026-10-10）
- 成片实测时长：__s
