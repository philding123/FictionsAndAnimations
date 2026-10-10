#!/usr/bin/env python3
"""全书分册工具：将 source/raw/全书_clean.txt 按 15 册拆分并生成章节索引。

用法:
    python tools/split_books.py

输出:
    source/text/卷01_权力的游戏_上.txt ... 卷15_魔龙的狂舞_下.txt
    source/chapters_index.json   （全部章节元数据：册、章序、POV、字数）
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source" / "raw" / "全书_clean.txt"
OUT = ROOT / "source" / "text"

# 非正文块过滤：卷间标记、册名、跋/附录/家谱、空块都不是章节
NONCHAPTER_PATTERNS = (
    re.compile(r"【第.+卷】"),
    re.compile(r"（[上中下]）\s*$"),
    re.compile(r"^附录|^跋$|后记"),
    re.compile(r"家族|世系表|度量衡|地图$"),
)


def is_chapter(pov: str, chars: int) -> bool:
    if chars < 300:
        return False
    return not any(p.search(pov) for p in NONCHAPTER_PATTERNS)

# 本套书内部的笔误「权利的游戏」统一修正为「权力的游戏」（仅用于文件命名）
BOOK_TITLES = {
    "1": "权力的游戏",
    "2": "列王的纷争",
    "3": "冰雨的风暴",
    "4": "群鸦的盛宴",
    "5": "魔龙的狂舞",
}
CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5}
PARTS = {"（上）": "上", "（中）": "中", "（下）": "下"}


def main():
    text = SRC.read_text(encoding="utf-8")
    pages = text.split("=====PAGEBREAK=====")

    vol_re = re.compile(r"【第([一二三四五])卷】")
    part_re = re.compile(r"^(.{2,10}?)（([上中下])）\s*$")

    # 定位每册起点（卷标记块的下一块是册名块，册内容从其后再下一块开始）
    starts = []  # (book_no, part, title_block_idx, content_start_idx)
    for i, p in enumerate(pages):
        s = p.strip()
        m = vol_re.search(s)
        if m and len(s) < 30:
            book_no = CN_NUM[m.group(1)]
            title = pages[i + 1].strip()
            pm = part_re.match(title)
            if pm:
                starts.append((book_no, pm.group(2), i, i + 2))

    if len(starts) != 15:
        raise SystemExit(f"错误: 期望 15 个分册标记，实际找到 {len(starts)} 个，中止拆分")

    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for seq, (book_no, part, t_idx, c_start) in enumerate(starts, 1):
        c_end = starts[seq][3] if seq < len(starts) else len(pages)
        blocks = [b.strip() for b in pages[c_start:c_end] if b.strip()]
        chapter_blocks = []
        for block in blocks:
            pov_line = block.split("\n")[0].strip()
            body = "\n".join(block.split("\n")[1:]).strip()
            if is_chapter(pov_line, len(body)):
                chapter_blocks.append((pov_line, body))
        title = BOOK_TITLES[str(book_no)]
        fname = f"卷{seq:02d}_{title}_{part}.txt"
        body_parts = []
        for ch_no, (pov, body) in enumerate(chapter_blocks, 1):
            body_parts.append(f"=====第{ch_no:03d}章 POV: {pov}=====\n\n{body}")
            index.append(
                {
                    "seq": seq,
                    "book": book_no,
                    "book_title": title,
                    "part": part,
                    "file": fname,
                    "chapter": ch_no,
                    "pov": pov,
                    "chars": len(body),
                }
            )
        (OUT / fname).write_text("\n\n".join(body_parts), encoding="utf-8")
        total = sum(c["chars"] for c in index if c["seq"] == seq)
        print(f"OK: {fname}  章节 {len(chapter_blocks)} 章  {total:,} 字")

    (ROOT / "source" / "chapters_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"索引: source/chapters_index.json  共 {len(index)} 章")


if __name__ == "__main__":
    main()
