#!/usr/bin/env python3
"""成片时长门禁：>600s 非零退出（PROJECT_SPEC R1）。

用法:
    python tools/check_duration.py <file.mp4> [上限秒数=600]

依赖 ffprobe（ffmpeg）；未安装时给出安装提示并以退出码 3 结束。
"""
import json
import shutil
import subprocess
import sys

DEFAULT_LIMIT = 600.0


def probe_duration(path: str) -> float:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        print("错误：未找到 ffprobe。请安装 ffmpeg（如 winget install Gyan.FFmpeg）后重试。")
        sys.exit(3)
    out = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "format=duration", "-of", "json", path],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        print(f"错误：ffprobe 读取失败：{out.stderr.strip()}")
        sys.exit(3)
    duration = float(json.loads(out.stdout)["format"]["duration"])
    return duration


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    limit = float(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_LIMIT
    duration = probe_duration(path)
    status = "PASS" if duration <= limit else "FAIL"
    print(f"[{status}] {path}  时长 {duration:.2f}s / 上限 {limit:.0f}s")
    sys.exit(0 if duration <= limit else 1)


if __name__ == "__main__":
    main()
