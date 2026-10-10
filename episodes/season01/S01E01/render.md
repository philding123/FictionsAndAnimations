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

## 后续：图生视频（真正渲染）

**工具链已选定：可灵（Kling）API，接入已打通（2026-10-10 实测）**：

- 端点 `https://api-beijing.klingai.com`（国内开发者平台；singapore/global 端点对国内 key 401）
- 凭证 `~/.config/Fiction/env` 的 KLING key（Bearer），鉴权验证通过
- 可用模型 `kling-v2-5-turbo`、`kling-v2-6`（旧型号已全部下线）
- 工具 `tools/gen_video_kling.py`（创建/轮询/下载）
- ⚠️ **当前 429 余额不足：API 额度与 App 会员独立**，待充值「API 资源包」后先跑
  pilot（kf-011 异鬼 5s std），按实测单价与耗时外推 79 镜总成本，经确认再批量生成。

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
