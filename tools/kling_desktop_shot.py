#!/usr/bin/env python3
"""可灵桌面端单镜自动化 v2：上传关键帧 → 填运镜提示词 → 生成 → 轮询 → 下载 → 归位。

用法:
    python tools/kling_desktop_shot.py --image <hd关键帧> --prompt-file <提示词.txt> \
        --out <seg/输出名.mp4> --tag <截图标签> [--wait 170]

前置：可灵桌面 App 已打开（任意页面）；运行期间不要动鼠标键盘。
坐标为 2560×1600 实测值，窗口勿移动/缩放。步骤截图存 .preview/batch_<tag>_stepN.png。
"""
import argparse
import shutil
import time
from pathlib import Path

import pyautogui
import pygetwindow as gw
import pyperclip
from PIL import ImageGrab

pyautogui.FAILSAFE = False
PREVIEW = Path(".preview")

POS = {
    "back_from_detail": (273, 210),    # 详情页左上角 ← 返回
    "video_tab": (534, 169),           # 视频生成页签
    "clear_thumb": (384, 1106),        # 首帧缩略图垃圾桶
    "upload_zone": (563, 538),         # 添加首尾帧（清空后的首帧位）
    "dialog_filename": (778, 787),     # 文件对话框文件名输入框
    "prompt_box": (725, 862),          # 提示词输入框
    "generate": (1007, 1404),          # 生成按钮
    "task_player": (1928, 785),        # 右侧任务卡播放器（点击开详情）
    "detail_download": (2048, 182),    # 详情页下载图标
    "watermark_save": (1643, 1171),    # 水印设置「保存设置」（如弹出）
}


def shot(tag: str, n: int):
    PREVIEW.mkdir(exist_ok=True)
    ImageGrab.grab().save(PREVIEW / f"batch_{tag}_step{n}.png")


def find_app():
    """按标题关键词找可灵 App 窗口（标题随页签变化，但必含这些词之一；
    注意脚本导入 pyautogui 后进程 DPI 感知，窗口尺寸为物理像素，不能按逻辑尺寸匹配）。"""
    import re

    pat = re.compile(r"可灵|kling|omni|视频|首页|创作", re.I)
    for w in gw.getAllWindows():
        if w.visible and w.width > 800 and pat.search(w.title or ""):
            return w
    return None


def newest_mp4_in_downloads(since: float):
    downloads = Path.home() / "Downloads"
    cands = [p for p in downloads.glob("*.mp4") if p.stat().st_mtime >= since]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--wait", type=int, default=170, help="生成轮询总时长(秒)")
    args = ap.parse_args()

    prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    app = find_app()
    if not app:
        raise SystemExit("错误：找不到可灵 App 窗口（标题应为「视频」）")
    try:
        app.activate()
    except Exception:
        app.restore()
    time.sleep(1.5)

    # 0) 若停在详情页则先返回，再确保在视频生成页签
    pyautogui.click(*POS["back_from_detail"])
    time.sleep(2)
    pyautogui.click(*POS["video_tab"])
    time.sleep(2)

    # 1) 清理上一镜残留（垃圾桶 + 清空提示词）
    pyautogui.click(*POS["clear_thumb"])
    time.sleep(1.2)
    pyautogui.click(*POS["prompt_box"])
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(0.8)
    shot(args.tag, 1)

    # 2) 上传首帧（原生对话框；等对话框完全弹出，防路径泄漏进提示词框）
    pyautogui.click(*POS["upload_zone"])
    time.sleep(3.5)
    pyautogui.click(*POS["dialog_filename"])
    time.sleep(0.8)
    pyautogui.write(str(Path(args.image).resolve()), interval=0.02)
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(7)
    shot(args.tag, 2)

    # 2.5) 兜底：再次清空提示词框（防止路径文本泄漏）
    pyautogui.click(*POS["prompt_box"])
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(0.6)

    # 3) 填提示词
    pyautogui.click(*POS["prompt_box"])
    time.sleep(0.6)
    pyperclip.copy(prompt)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1.5)
    shot(args.tag, 3)

    # 4) 生成
    pyautogui.click(*POS["generate"])
    time.sleep(6)
    shot(args.tag, 4)

    # 5) 轮询等待完成（固定时长，产物以下载落盘为准）
    deadline = time.time() + args.wait
    while time.time() < deadline:
        time.sleep(20)
    shot(args.tag, 5)

    # 6) 打开详情页并下载
    pyautogui.click(*POS["task_player"])
    time.sleep(2.5)
    pyautogui.click(*POS["detail_download"])
    time.sleep(3)
    pyautogui.click(*POS["watermark_save"])  # 若无弹窗则点在空白处，无害
    time.sleep(3)
    shot(args.tag, 6)

    # 7) 等待文件落盘并归位
    t0 = time.time()
    src = None
    while time.time() - t0 < 40:
        src = newest_mp4_in_downloads(t0)
        if src:
            break
        time.sleep(4)
    if not src:
        shot(args.tag, 7)
        raise SystemExit(f"错误：下载未落盘，请查看 batch_{args.tag}_step5/6/7.png")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(out))
    print(f"OK: {out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
