#!/usr/bin/env python3
"""动态分镜（animatic）构建器：HD 关键帧 + Ken Burns 运镜 → 按分段表合成 mp4。

用法:
    python tools/build_animatic.py episodes/season01/S01E01

依赖 <集目录>/seg/segments.json（分段表）与 keyframes/hd/（1920×1080 基准帧）、
ffmpeg（PATH 或 WINGET_LOCATIONS 可发现）。输出 <集目录>/seg/<集号>_animatic.mp4，
随后用 tools/check_duration.py 过门禁。
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FPS = 24
PRESCALE = 3840  # 放大后再 zoompan，减小抖动

MOTIONS = {
    # zoom 表达式；N=总帧数；x/y 默认居中
    "push-in":   "min(1+0.12*on/{N},1.12)",
    "slow-push": "min(1+0.06*on/{N},1.06)",
    "pull-out":  "max(1.12-0.12*on/{N},1.0)",
    "pan-right": "1.10",
    "pan-left":  "1.10",
}


def pan_xy(motion: str) -> tuple[str, str]:
    if motion == "pan-right":
        return ("(iw-iw/zoom)*on/{N}", "ih/2-(ih/zoom/2)")
    if motion == "pan-left":
        return ("(iw-iw/zoom)*(1-on/{N})", "ih/2-(ih/zoom/2)")
    return ("iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)")  # 居中推拉


def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    # winget 安装后当前会话 PATH 可能未刷新：探测 FFMPEG_WINGET 或默认链接目录
    candidates = [
        Path.home() / "AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe",
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-*/bin/ffmpeg.exe",
    ]
    import glob as g
    for c in candidates:
        hits = g.glob(str(c))
        if hits:
            return str(hits[0])
    # pip static-ffmpeg（项目当前的实际安装途径）
    try:
        from static_ffmpeg import run as sf

        ffmpeg, _ = sf.get_or_fetch_platform_executables_else_raise()
        return ffmpeg
    except Exception:
        raise SystemExit("错误：找不到 ffmpeg；请 pip install static-ffmpeg 后重试")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    ep = Path(sys.argv[1])
    spec = json.loads((ep / "seg" / "segments.json").read_text(encoding="utf-8"))
    fps = spec.get("fps", FPS)
    w, h = spec.get("width", 1920), spec.get("height", 1080)
    ffmpeg = find_ffmpeg()
    seg_dir = ep / "seg"
    tmp = Path(tempfile.mkdtemp(prefix="animatic_"))
    concat_list = tmp / "list.txt"

    try:
        total = 0
        for i, s in enumerate(spec["segments"], 1):
            img = ep / "keyframes" / "hd" / s["img"]
            dur = float(s["seconds"])
            total += dur
            n = round(dur * fps)
            z = MOTIONS[s["motion"]].format(N=n)
            px, py = pan_xy(s["motion"])
            vf = (
                f"scale={PRESCALE}:-2,"
                f"zoompan=z='{z}':x='{px.format(N=n)}':y='{py.format(N=n)}':"
                f"d={n}:s={w}x{h}:fps={fps},format=yuv420p"
            )
            out_seg = tmp / f"seg{i:02d}.mp4"
            cmd = [ffmpeg, "-y", "-loop", "1", "-framerate", str(fps),
                   "-i", str(img), "-vf", vf, "-frames:v", str(n),
                   "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                   str(out_seg)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(r.stderr[-1500:])
                raise SystemExit(f"错误：分段 {i} 编码失败")
            print(f"seg{i:02d}: {s['img']} {dur}s [{s['motion']}] -> {out_seg.name}")
            with open(concat_list, "a", encoding="utf-8") as f:
                f.write(f"file '{out_seg.as_posix()}'\n")

        final = seg_dir / f"{ep.name}_animatic.mp4"
        r = subprocess.run(
            [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
             "-c", "copy", str(final)], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-1500:])
            raise SystemExit("错误：concat 失败")
        print(f"OK: {final}  预算总时长 {total}s（{len(spec['segments'])} 段）")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
