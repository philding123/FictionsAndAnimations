#!/usr/bin/env python3
"""MOBI HTML 清洗工具：剥离标签，输出带分页标记的纯文本。

用法:
    python tools/clean_html.py <input.html> <output.txt>

- <mbp:pagebreak/> 转换为 \n\n=====PAGEBREAK=====\n\n（章节/分卷边界参考）
- 其余标签剥离，段落间保留换行
"""
import re
import sys
from pathlib import Path


def clean(html: str) -> str:
    html = re.sub(r"<mbp:pagebreak[^>]*/?>", "\n\n=====PAGEBREAK=====\n\n", html)
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = re.sub(r"</p\s*>", "\n\n", html)
    html = re.sub(r"<[^>]+>", "", html)
    import html as htmllib

    html = htmllib.unescape(html)
    # PalmDOC 解压残留的控制字符（含 \x00）一并清除，仅保留换行/制表
    html = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", html)
    html = re.sub(r"[ \t\u3000]+", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = clean(src.read_text(encoding="utf-8"))
    dst.write_text(text, encoding="utf-8")
    print(f"OK: {dst}  字符数: {len(text):,}  分页数: {text.count('=====PAGEBREAK=====')}")


if __name__ == "__main__":
    main()
