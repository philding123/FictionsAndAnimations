#!/usr/bin/env python3
"""E01 成片拼装 v1：动态分镜 + 已有图生视频片段 → 541s 成片。

用法:
    python tools/assemble_final.py

规则（基于 episodes/season01/S01E01/seg/segments.json）：
- 场景若存在 seg/kling_<kf>.mp4（图生视频片段），则场景结构为
  [KB 引导 (dur-real)/2] + [真实片段] + [KB 收尾 (dur-real)/2]；
- 否则整段 KB 运镜。
输出: seg/S01E01_cut_v1.mp4（1920×1080/24fps/H.264，含静音轨）
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from static_ffmpeg import run as sf

EP = Path("episodes/season01/S01E01")
FPS = 24
W, H = 1920, 1080

# 已入库的图生视频片段（场景 kf → 片段文件）
REAL = {
    "kf-011": EP / "seg/kling_pilot_kf-011.mp4",
    "kf-001": EP / "seg/kling_kf-001.mp4",
    "kf-024": EP / "seg/kling_kf-024.mp4",
}


def ff():
    return sf.get_or_fetch_platform_executables_else_raise()[0]


def fprobe():
    return sf.get_or_fetch_platform_executables_else_raise()[1]


def probe_duration(path: Path) -> float:
    probe = subprocess.run([fprobe(), "-v", "error", "-show_entries",
                            "format=duration", "-of", "json",
                            str(path)], capture_output=True, text=True)
    import json as j
    return float(j.loads(probe.stdout)["format"]["duration"])


def kb_segment(ffmpeg, img: Path, dur: float, out: Path, motion="push"):
    n = round(dur * FPS)
    if motion == "pull":
        z = f"max(1.12-0.12*on/{n},1.0)"
    else:
        z = f"min(1+0.10*on/{n},1.10)"
    vf = (
        f"scale=3840:-2,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={n}:s={W}x{H}:fps={FPS},format=yuv420p"
    )
    r = subprocess.run([ffmpeg, "-y", "-loop", "1", "-framerate", str(FPS),
                        "-i", str(img), "-vf", vf, "-frames:v", str(n),
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        str(out)], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:])
        raise SystemExit(f"KB 段失败: {out}")


def main():
    ffmpeg = ff()
    spec = json.loads((EP / "seg/segments.json").read_text(encoding="utf-8"))
    tmp = Path(tempfile.mkdtemp(prefix="assemble_"))
    concat = tmp / "list.txt"
    total = 0
    try:
        for i, s in enumerate(spec["segments"], 1):
            kf = s["img"].replace(".png", "")
            dur = float(s["seconds"])
            total += dur
            real = REAL.get(kf)
            parts = []
            if real and real.exists():
                rdur = probe_duration(real)
                lead = round((dur - rdur) / 2, 2)
                tail = round(dur - rdur - lead, 2)
                if lead > 0.3:
                    kb_segment(ffmpeg, EP / "keyframes/hd" / s["img"], lead,
                               tmp / f"sc{i:02d}_a.mp4", "push")
                    parts.append(tmp / f"sc{i:02d}_a.mp4")
                # 真实片段（统一到 1080p24）
                r = subprocess.run([ffmpeg, "-y", "-i", str(real),
                                    "-vf", f"scale={W}:{H},fps={FPS},format=yuv420p",
                                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                                    str(tmp / f"sc{i:02d}_real.mp4")],
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    print(r.stderr[-500:])
                    raise SystemExit("真实片段转码失败")
                parts.append(tmp / f"sc{i:02d}_real.mp4")
                if tail > 0.3:
                    kb_segment(ffmpeg, EP / "keyframes/hd" / s["img"], tail,
                               tmp / f"sc{i:02d}_b.mp4", "pull")
                    parts.append(tmp / f"sc{i:02d}_b.mp4")
                print(f"scene{i} ({kf}): KB {lead}s + REAL {rdur:.2f}s + KB {tail}s")
            else:
                kb_segment(ffmpeg, EP / "keyframes/hd" / s["img"], dur,
                           tmp / f"sc{i:02d}_full.mp4", "push" if i % 2 else "pull")
                parts.append(tmp / f"sc{i:02d}_full.mp4")
                print(f"scene{i} ({kf}): KB {dur}s（无真实片段）")
            for p in parts:
                with open(concat, "a", encoding="utf-8") as f:
                    f.write(f"file '{p.as_posix()}'\n")

        out = EP / "seg/S01E01_cut_v1.mp4"
        # 拼接 + 静音轨（播放器兼容）
        r = subprocess.run([ffmpeg, "-y", "-f", "concat", "-safe", "0",
                            "-i", str(concat),
                            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                            "-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                            str(out)], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-800:])
            raise SystemExit("拼接失败")
        print(f"OK: {out}  预算 {total}s")
    finally:
        shutil = __import__("shutil")
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
