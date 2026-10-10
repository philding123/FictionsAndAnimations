#!/usr/bin/env python3
"""关键帧归一化：缩放覆盖 + 居中裁切到 1920×1080（渲染管线基准分辨率）。

用法:
    python tools/normalize_keyframes.py [集目录]

缺省处理 episodes/season01/S01E01；输出写入 <集目录>/keyframes/hd/。
算法：Lanczos 等比放大至覆盖 1920×1080，居中裁切（AI 关键帧无真超分模型时的
确定性基准化步骤；后续接入 Real-ESRGAN 类工具可替换实现，接口不变）。
"""
import sys
from pathlib import Path

from PIL import Image

W, H = 1920, 1080


def normalize(src: Path, dst: Path) -> tuple[int, int]:
    im = Image.open(src).convert("RGB")
    ow, oh = im.size
    scale = max(W / ow, H / oh)
    nw, nh = round(ow * scale), round(oh * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - W) // 2, (nh - H) // 2
    im = im.crop((left, top, left + W, top + H))
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "PNG")
    return ow, oh


def main():
    ep = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "episodes/season01/S01E01")
    kf = ep / "keyframes"
    outs = sorted(kf.glob("kf-*.png"))
    if not outs:
        raise SystemExit(f"错误：{kf} 下没有 kf-*.png")
    for src in outs:
        ow, oh = normalize(src, kf / "hd" / src.name)
        print(f"OK: hd/{src.name}  {ow}x{oh} -> {W}x{H}")
    print(f"完成：{len(outs)} 张 -> {kf / 'hd'}")


if __name__ == "__main__":
    main()
