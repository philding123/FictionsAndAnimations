#!/usr/bin/env python3
"""MOBI (PalmDOC, MOBI7) 提取工具：将 .mobi 正文解压为 UTF-8 文本。

用法:
    python tools/extract_mobi.py <input.mobi> <output.txt>

仅支持 PalmDOC 压缩 (compression=1/2)、无加密的 MOBI7 文件；
HUFF/CDIC (compression=17480) 或 DRM 文件会明确报错退出。
"""
import struct
import sys
from pathlib import Path


def parse_pdb(data: bytes):
    num_records = struct.unpack(">H", data[76:78])[0]
    offsets = [
        struct.unpack(">I", data[78 + i * 8 : 82 + i * 8])[0]
        for i in range(num_records)
    ]
    offsets.append(len(data))
    return [data[offsets[i] : offsets[i + 1]] for i in range(num_records)]


def parse_mobi_header(rec0: bytes):
    compression, _unused, text_len, text_rec_count, _rec_size, encryption = (
        struct.unpack(">HHIHHH", rec0[:14])
    )
    if rec0[16:20] != b"MOBI":
        raise SystemExit("错误: 缺少 MOBI 魔数，不是 MOBI 格式")
    header_len = struct.unpack(">I", rec0[20:24])[0]
    encoding = struct.unpack(">I", rec0[28:32])[0]
    return compression, text_len, text_rec_count, encryption, encoding


def palmdoc_decompress(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        b = data[i]
        i += 1
        if b == 0:
            out.append(0)
        elif b <= 8:
            out += data[i : i + b]
            i += b
        elif b <= 0x7F:
            out.append(b)
        elif b <= 0xBF:
            if i >= n:
                break
            b2 = data[i]
            i += 1
            pair = (b << 8) | b2
            distance = (pair >> 3) & 0x7FF
            length = (pair & 0x7) + 3
            for _ in range(length):
                out.append(out[-distance])
        else:  # 0xC0..0xFF
            out += b" "
            out.append(b ^ 0x80)
    return bytes(out)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    records = parse_pdb(src.read_bytes())
    compression, text_len, text_rec_count, encryption, encoding = parse_mobi_header(
        records[0]
    )
    if encryption != 0:
        raise SystemExit(f"错误: 文件已加密 (encryption={encryption})，无法提取")
    if compression not in (1, 2):
        raise SystemExit(
            f"错误: 压缩类型 {compression} (HUFF/CDIC) 暂不支持，仅支持 PalmDOC"
        )
    codec = "utf-8" if encoding == 65001 else "mbcs"
    chunks = []
    for rec in records[1 : 1 + text_rec_count]:
        chunks.append(rec if compression == 1 else palmdoc_decompress(rec))
    raw = b"".join(chunks)[:text_len]
    text = raw.decode(codec, errors="replace")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    print(f"OK: {dst}  正文字符数: {len(text):,}  编码: {codec}")


if __name__ == "__main__":
    main()
