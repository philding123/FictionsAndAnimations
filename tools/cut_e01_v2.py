#!/usr/bin/env python3
"""E01 v2 切割装配：《长城之外》纯北境开幕，360s，含字卡/旁白/环境音。

时间轴（总 360s）：
  000-002 黑场 ｜ 002-074 S1 序幕森林(KB+REAL kf-001) ｜ 074-156 S2 异鬼(KB+REAL kf-011)
  156-161 片名卡 ｜ 161-267 S3 处决(KB+REAL kf-024) ｜ 267-347 S4 母狼(KB kf-039)
  347-360 片尾字卡
音频：环境风声底(全片) + Huihui TTS 旁白(开场/片尾)。
输出: seg/S01E01_final_v2.mp4
"""
import subprocess
import tempfile
import time
from pathlib import Path

from static_ffmpeg import run as sf

EP = Path("episodes/season01/S01E01")
FPS, W, H = 24, 1920, 1080
FONT = "C\\:/Windows/Fonts/msyh.ttc"


def fftools():
    ff, fp = sf.get_or_fetch_platform_executables_else_raise()
    return ff, fp


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-600:])
        raise SystemExit(f"命令失败: {cmd[:3]}")


def kb(out, img, dur, motion="push"):
    n = round(dur * FPS)
    z = (f"max(1.10-0.10*on/{n},1.0)" if motion == "pull"
         else f"min(1+0.08*on/{n},1.08)")
    vf = (f"scale=3840:-2,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':"
          f"y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},format=yuv420p")
    run([ffmpeg, "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(img),
         "-vf", vf, "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", str(out)])


def real(out, src):
    run([ffmpeg, "-y", "-i", str(src),
         "-vf", f"scale={W}:{H},fps={FPS},format=yuv420p",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)])


def card(out, dur, line1, line2=""):
    """用 PIL 渲染字卡 PNG（避免 ffmpeg drawtext 转义问题），再 loop 成视频。"""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (W, H), (13, 14, 16))
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 96)
    f2 = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 40)
    d.text((W / 2, H / 2 - 70), line1, font=f1, fill=(232, 230, 224), anchor="mm")
    if line2:
        d.text((W / 2, H / 2 + 60), line2, font=f2, fill=(155, 160, 164), anchor="mm")
    png = out.with_suffix(".png")
    img.save(png)
    run([ffmpeg, "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(png),
         "-frames:v", str(round(dur * FPS)), "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", str(out)])
    png.unlink()


def tts(out, text, rate=-2):
    ps = (
        "Add-Type -AssemblyName System.Speech;"
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        f"$s.SelectVoice('Microsoft Huihui Desktop');"
        f"$s.Rate = {rate};"
        f"$s.SetOutputToWaveFile('{out.as_posix()}');"
        f"$s.Speak('{text}');"
        "$s.Dispose()"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-300:])
        raise SystemExit("TTS 失败")


def main():
    global ffmpeg
    ffmpeg, ffprobe = sf.get_or_fetch_platform_executables_else_raise()
    tmp = Path(tempfile.mkdtemp(prefix="e01v2_"))
    hd = EP / "keyframes/hd"
    concat = tmp / "list.txt"
    t0 = time.time()

    # 旁白 TTS（PowerShell 输出 44k wav 可能带头，后续混音时统一处理）
    n1 = tmp / "nar_open.wav"
    n2 = tmp / "nar_end.wav"
    tts(n1, "长城之外，是七国忘却的地方。")
    tts(n2, "凛冬将至。")
    print(f"TTS ok  ({time.time()-t0:.0f}s)")

    # 视频段
    segs = []
    def add(p):
        segs.append(p)
        with open(concat, "a", encoding="utf-8") as f:
            f.write(f"file '{p.as_posix()}'\n")

    black = tmp / "seg00_black.mp4"
    run([ffmpeg, "-y", "-f", "lavfi", "-i", f"color=c=0x0D0E10:s={W}x{H}:d=2:r={FPS}",
         "-frames:v", str(2 * FPS), "-c:v", "libx264", "-crf", "18", str(black)])
    add(black)

    kb(tmp / "seg01.mp4", hd / "kf-001.png", 68.54, "push"); add(tmp / "seg01.mp4")
    real(tmp / "seg02.mp4", EP / "seg/kling_kf-001.mp4"); add(tmp / "seg02.mp4")
    kb(tmp / "seg03.mp4", hd / "kf-011.png", 38.48, "push"); add(tmp / "seg03.mp4")
    real(tmp / "seg04.mp4", EP / "seg/kling_pilot_kf-011.mp4"); add(tmp / "seg04.mp4")
    kb(tmp / "seg05.mp4", hd / "kf-011.png", 38.48, "pull"); add(tmp / "seg05.mp4")
    card(tmp / "seg06_title.mp4", 5, "凛 冬 将 至", "STARK · WINTERFELL"); add(tmp / "seg06_title.mp4")
    kb(tmp / "seg07.mp4", hd / "kf-024.png", 50.48, "push"); add(tmp / "seg07.mp4")
    real(tmp / "seg08.mp4", EP / "seg/kling_kf-024.mp4"); add(tmp / "seg08.mp4")
    kb(tmp / "seg09.mp4", hd / "kf-024.png", 50.48, "pull"); add(tmp / "seg09.mp4")
    kb(tmp / "seg10.mp4", hd / "kf-039.png", 80.0, "push"); add(tmp / "seg10.mp4")
    card(tmp / "seg11_end.mp4", 13, "凛 冬 将 至", "下集 · 国王驾到"); add(tmp / "seg11_end.mp4")
    print(f"video segments ok  ({time.time()-t0:.0f}s)")

    # 音频：环境风声底 + 旁白定址混音
    ambient = tmp / "ambient.wav"
    run([ffmpeg, "-y", "-f", "lavfi",
         "-i", "anoisesrc=color=pink:amplitude=0.5:duration=360:sample_rate=44100",
         "-af", "highpass=f=120,lowpass=f=600,volume=0.5", str(ambient)])
    a1 = tmp / "nar_open.wav"
    a2 = tmp / "nar_end.wav"
    mix_cmd = [
        ffmpeg, "-y",
        "-i", str(ambient), "-i", str(a1), "-i", str(a2),
        "-filter_complex",
        "[1:a]volume=1.0,adelay=4000|4000[n1];"
        "[2:a]volume=1.0,adelay=347000|347000[n2];"
        "[0:a]volume=0.5[amb];[amb][n1][n2]amix=inputs=3:duration=first:normalize=0[aout]",
        "-map", "0:v?", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
        str(tmp / "audio.m4a"),
    ]
    run(mix_cmd)

    # 合成：视频 concat + 音频
    out = EP / "seg/S01E01_final_v2.mp4"
    r = subprocess.run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                        "-i", str(tmp / "audio.m4a"), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "copy", "-shortest", str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:])
        raise SystemExit("合成失败")
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"OK: {out}  ({out.stat().st_size // 1024 // 1024} MB)  用时 {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
