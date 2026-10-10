#!/usr/bin/env python3
"""通过 CDP 控制用户本机 Chrome（可灵会员已登录的真实浏览器）。

前置：Chrome 以 --remote-debugging-port=9222 启动。
用法:
    python tools/cdp_kling.py status                 # 列出打开的标签页
    python tools/cdp_kling.py goto <url>             # 在 klingai 标签页导航
    python tools/cdp_kling.py snapshot [前N字符]     # 当前页 ARIA 快照
    python tools/cdp_kling.py upload <图片路径>      # 注入图片到 el-upload 控件
    python tools/cdp_kling.py fill <文本>            # 填提示词输入框
    python tools/cdp_kling.py click <文本>           # 按可见文本点击
    python tools/cdp_kling.py eval <js表达式>        # 页面内执行 JS
"""
import sys
import time

from playwright.sync_api import sync_playwright

CDP = "http://localhost:9222"


def find_kling_page(pages):
    for p in pages:
        if "klingai.com" in p.url:
            return p
    return pages[0] if pages else None


def connect():
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(CDP)
    ctx = browser.contexts[0]
    page = find_kling_page(ctx.pages)
    if page is None:
        page = ctx.new_page()
        page.goto("https://klingai.com/app")
    return pw, browser, page


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    pw, browser, page = connect()
    try:
        if cmd == "status":
            for ctx in browser.contexts:
                for p in ctx.pages:
                    print(f"- {p.url}  |  {p.title()[:60]}")
        elif cmd == "goto":
            page.goto(arg)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(3)
            print("URL:", page.url)
        elif cmd == "snapshot":
            n = int(arg) if arg else 3000
            print(page.locator("body").aria_snapshot()[:n])
        elif cmd == "upload":
            page.wait_for_selector("input.el-upload__input", timeout=10000)
            page.set_input_files("input.el-upload__input", arg)
            time.sleep(5)
            print("已注入:", arg)
        elif cmd == "fill":
            page.locator("textarea").first.fill(arg)
            print("已填提示词")
        elif cmd == "click":
            page.get_by_text(arg, exact=True).first.click()
            time.sleep(2)
            print("已点击:", arg)
        elif cmd == "eval":
            print(page.evaluate(arg))
        else:
            print(f"未知命令: {cmd}")
            sys.exit(2)
    finally:
        pw.stop()


if __name__ == "__main__":
    main()
