#!/usr/bin/env python3
"""角色设定图生成器：characters/roster.json → 每角色 sheet.svg + design.md（自动区）。

用法:
    python tools/gen_character_sheet.py [角色id ...]   # 缺省全量生成

确定性：同 roster.json 输入必产出逐字节相同的 SVG（无时间戳）。
design.md：文件不存在则创建；存在则只替换 <!-- AUTO:BEGIN/END --> 标记区，保留手写内容。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "characters" / "roster.json"
OUT_DIR = ROOT / "characters"

FONT = '"Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif'
FONT_MONO = 'Consolas, "Courier New", monospace'
W, H = 900, 1200

REQ = ("id name_zh name_en house house_color role age_look build face hair "
       "palette costume features demeanor first_episode design_version").split()
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
LENGTHS = {"short", "medium", "long"}
MOUTHS = {"neutral", "firm", "smirk", "frown"}
SHAPES = {"long", "oval", "round"}
FACIALS = {"none", "stubble", "goatee", "thick_beard"}


def validate(c):
    for k in REQ:
        if k not in c:
            raise SystemExit(f"[{c.get('id','?')}] 缺少必填字段: {k}")
    for k in ("skin_hex", "eye_hex"):
        if not HEX_RE.match(c["face"][k]):
            raise SystemExit(f"[{c['id']}] face.{k} 非法 hex: {c['face'][k]}")
    if not HEX_RE.match(c["hair"]["hex"]) or not HEX_RE.match(c["house_color"]):
        raise SystemExit(f"[{c['id']}] hair.hex / house_color 非法")
    if len(c["palette"]) != 5:
        raise SystemExit(f"[{c['id']}] palette 必须 5 项")
    for p in c["palette"]:
        if not HEX_RE.match(p["hex"]):
            raise SystemExit(f"[{c['id']}] palette 非法 hex: {p['hex']}")
    if c["hair"]["length"] not in LENGTHS:
        raise SystemExit(f"[{c['id']}] hair.length 必须是 {LENGTHS}")
    if c["face"]["mouth"] not in MOUTHS:
        raise SystemExit(f"[{c['id']}] face.mouth 必须是 {MOUTHS}")
    if c["face"]["shape"] not in SHAPES:
        raise SystemExit(f"[{c['id']}] face.shape 必须是 {SHAPES}")
    if c["hair"]["facial"] not in FACIALS:
        raise SystemExit(f"[{c['id']}] hair.facial 必须是 {FACIALS}")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


CLOSERS = "，。；、）】」』！？：…"


def wrap(text, width=16):
    """中文按字符宽换行；收尾标点不落行首；不拆 ASCII 单词。"""
    lines, cur = [], ""
    for idx, ch in enumerate(text):
        cur += ch
        if len(cur) >= width:
            nxt = text[idx + 1] if idx + 1 < len(text) else ""
            if nxt and nxt in CLOSERS:
                continue  # 把收尾标点并入本行
            m = re.search(r"[A-Za-z0-9]+$", cur)
            if m and nxt and re.match(r"[A-Za-z0-9]", nxt):
                word = m.group(0)
                lines.append(cur[: len(cur) - len(word)])
                cur = word
            else:
                lines.append(cur)
                cur = ""
    if cur:
        lines.append(cur)
    return lines


def darken(hex_color, f=0.72):
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return f"#{int(r*f):02X}{int(g*f):02X}{int(b*f):02X}"


def lighten(hex_color, f=1.18):
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return f"#{min(255,int(r*f)):02X}{min(255,int(g*f)):02X}{min(255,int(b*f)):02X}"


# ---------------------------------------------------------------- portrait --
def portrait_svg(c):
    cx = 290
    ry = {"long": 86, "oval": 82, "round": 78}[c["face"]["shape"]]
    rx = {"long": 66, "oval": 70, "round": 76}[c["face"]["shape"]]
    cy = 330
    skin = c["face"]["skin_hex"]
    hair_hex = c["hair"]["hex"]
    eye_hex = c["face"]["eye_hex"]
    pal = c["palette"]
    p = []

    # --- 剪影级体型参数
    sw = {"ned-stark": 212, "catelyn-stark": 168, "robb-stark": 200,
          "sansa-stark": 156, "arya-stark": 138, "bran-stark": 132,
          "jon-snow": 182, "daenerys-targaryen": 160, "tyrion-lannister": 150,
          "cersei-lannister": 168, "jaime-lannister": 202,
          "robert-baratheon": 252, "khal-drogo": 262,
          "joffrey-baratheon": 150}.get(c["id"], 190)
    is_dress = c["id"] in ("catelyn-stark", "sansa-stark", "daenerys-targaryen",
                           "cersei-lannister")
    is_child = c["id"] in ("arya-stark", "bran-stark", "sansa-stark",
                           "joffrey-baratheon")
    floor = 935
    torso_top = 448
    hip_w = sw * (0.38 if is_dress else 0.46)

    # --- 背景光晕（厚涂底）
    p.append(f'<ellipse cx="{cx}" cy="600" rx="330" ry="420" fill="{c["house_color"]}" opacity="0.10"/>')

    # --- 披风（躯干后面）
    if "披风" in c["costume"]:
        cape = pal[1]["hex"]
        p.append(
            f'<path d="M {cx-sw*0.30} 470 C {cx-sw*0.52} 560 {cx-sw*0.56} 760 {cx-sw*0.60} {floor-8} '
            f'L {cx+sw*0.60} {floor-8} C {cx+sw*0.56} 760 {cx+sw*0.52} 560 {cx+sw*0.30} 470 Z" fill="{cape}"/>'
            f'<path d="M {cx-sw*0.30} 470 C {cx-sw*0.52} 560 {cx-sw*0.56} 760 {cx-sw*0.60} {floor-8} '
            f'L {cx-sw*0.42} {floor-8} C {cx-sw*0.40} 720 {cx-sw*0.36} 560 {cx-sw*0.24} 476 Z" fill="#000000" opacity="0.22"/>'
        )

    # --- 后层长发
    if c["hair"]["length"] == "long":
        hw = rx + 30
        p.append(
            f'<path d="M {cx} {cy-ry-8} C {cx-hw} {cy-ry} {cx-hw} {cy+40} {cx-hw+4} {cy+150} '
            f'C {cx-hw+2} {cy+210} {cx-hw+10} {cy+215} {cx-hw+6} 500 L {cx+hw-6} 500 '
            f'C {cx+hw-10} {cy+215} {cx+hw-2} {cy+210} {cx+hw-4} {cy+150} '
            f'C {cx+hw} {cy+40} {cx+hw} {cy-ry} {cx} {cy-ry-8} Z" fill="{darken(hair_hex,0.85)}"/>'
        )
    elif c["hair"]["length"] == "medium":
        hw = rx + 16
        p.append(
            f'<path d="M {cx} {cy-ry-6} C {cx-hw} {cy-ry+2} {cx-hw} {cy+30} {cx-hw+2} {cy+ry+26} '
            f'L {cx+hw-2} {cy+ry+26} C {cx+hw} {cy+30} {cx+hw} {cy-ry+2} {cx} {cy-ry-6} Z" '
            f'fill="{darken(hair_hex,0.85)}"/>'
        )

    # --- 颈与肩躯干
    p.append(f'<rect x="{cx-21}" y="{cy+ry-24}" width="42" height="{torso_top-cy-ry+34}" rx="12" fill="{darken(skin,0.88)}"/>')
    p.append(f'<path d="M {cx-21} {cy+ry+6} Q {cx} {cy+ry+26} {cx+21} {cy+ry+6} L {cx+21} {torso_top} L {cx-21} {torso_top} Z" fill="#000000" opacity="0.25"/>')

    torso = (
        f'M {cx-52} {torso_top-14} C {cx-sw/2:.0f} {torso_top+14} {cx-sw/2:.0f} {torso_top+26} {cx-sw/2+6:.0f} 540 '
        f'L {cx-hip_w:.0f} {floor-6} L {cx+hip_w:.0f} {floor-6} L {cx+sw/2-6:.0f} 540 '
        f'C {cx+sw/2:.0f} {torso_top+26} {cx+sw/2:.0f} {torso_top+14} {cx+52} {torso_top-14} Z'
    )
    p.append(f'<path d="{torso}" fill="{pal[0]["hex"]}"/>')
    # 躯干左侧体积阴影（厚涂式暗部）
    p.append(f'<path d="{torso}" fill="url(#torsoShade)"/>')
    # 中缝/系带结构线
    p.append(f'<path d="M {cx} {torso_top+6} L {cx} {floor-14}" stroke="#000000" stroke-opacity="0.28" stroke-width="3"/>')
    # V 领 + 家族色领缘
    p.append(f'<path d="M {cx-40} {torso_top-10} L {cx} {torso_top+88} L {cx+40} {torso_top-10}" fill="none" stroke="{c["house_color"]}" stroke-width="7" stroke-linejoin="round"/>')

    # --- 裙装（女性）：腰线以下外扩
    if is_dress:
        p.append(
            f'<path d="M {cx-hip_w:.0f} 640 C {cx-sw*0.72:.0f} 780 {cx-sw*0.78:.0f} 880 {cx-sw*0.72:.0f} {floor-4} '
            f'L {cx+sw*0.72:.0f} {floor-4} C {cx+sw*0.78:.0f} 880 {cx+sw*0.72:.0f} 780 {cx+hip_w:.0f} 640 Z" '
            f'fill="{pal[0]["hex"]}"/>'
            f'<path d="M {cx-hip_w:.0f} 640 C {cx-sw*0.72:.0f} 780 {cx-sw*0.78:.0f} 880 {cx-sw*0.72:.0f} {floor-4} '
            f'L {cx-sw*0.52:.0f} {floor-4} C {cx-sw*0.50:.0f} 840 {cx-sw*0.46:.0f} 760 {cx-hip_w+16:.0f} 648 Z" '
            f'fill="#000000" opacity="0.20"/>'
        )
        p.append(f'<rect x="{cx-hip_w-4:.0f}" y="630" width="{hip_w*2+8:.0f}" height="20" rx="8" fill="{pal[3]["hex"]}"/>')
    else:
        # 腰带
        p.append(f'<rect x="{cx-hip_w-6:.0f}" y="686" width="{hip_w*2+12:.0f}" height="26" rx="6" fill="{pal[2]["hex"]}"/>')
        p.append(f'<rect x="{cx-14}" y="684" width="28" height="30" rx="4" fill="{pal[3]["hex"]}"/>')

    # --- 护甲层（仅当主服装色即甲：如詹姆的金甲）
    if "甲" in pal[0]["name"]:
        metal = pal[3]["hex"]
        p.append(f'<path d="M {cx-sw*0.40:.0f} 520 Q {cx} 496 {cx+sw*0.40:.0f} 520 L {cx+sw*0.34:.0f} 700 Q {cx} 724 {cx-sw*0.34:.0f} 700 Z" fill="{lighten(pal[0]["hex"],1.12)}"/>')
        p.append(f'<path d="M {cx} 508 L {cx} 716" stroke="{darken(metal,0.7)}" stroke-width="5"/>')
        p.append(f'<ellipse cx="{cx-sw/2+14:.0f}" cy="498" rx="28" ry="19" fill="{metal}"/>')
        p.append(f'<ellipse cx="{cx+sw/2-14:.0f}" cy="498" rx="28" ry="19" fill="{darken(metal,0.85)}"/>')
        p.append(f'<circle cx="{cx-sw/2+14:.0f}" cy="498" r="8" fill="{darken(metal,0.55)}"/>')
        p.append(f'<circle cx="{cx+sw/2-14:.0f}" cy="498" r="8" fill="{darken(metal,0.55)}"/>')

    # --- 多斯拉克皮革甲带（卓戈：对称双带）
    if c["id"] == "khal-drogo":
        for side in (-1, 1):
            x0 = cx + side * sw * 0.22
            p.append(f'<path d="M {x0-side*10:.0f} {torso_top-6} L {x0+side*16:.0f} 690 L {x0+side*44:.0f} 690 L {x0+side*18:.0f} {torso_top-6} Z" fill="{pal[1]["hex"]}"/>')
            p.append(f'<circle cx="{x0+side*30:.0f}" cy="600" r="7" fill="none" stroke="{pal[2]["hex"]}" stroke-width="3.5"/>')

    # --- 毛领 / 披风扣
    if "披风" in c["costume"] or "毛" in c["costume"]:
        pts_l, pts_r = [], []
        n = 7
        for i in range(n + 1):
            x = cx - 66 + i * (132 / n)
            y = 505 + (14 if i % 2 else 0)
            (pts_r if x >= cx else pts_l).append((x, y))
        poly = f'{cx-66} 462 ' + " ".join(f"{x:.0f} {y:.0f}" for x, y in pts_l) + " "
        poly += " ".join(f"{x:.0f} {y:.0f}" for x, y in pts_r) + f' {cx+66} 462'
        p.append(f'<polygon points="{poly}" fill="{pal[1]["hex"]}"/>')
        p.append(f'<circle cx="{cx-sw/2+30:.0f}" cy="478" r="12" fill="{pal[3]["hex"]}"/>')

    # --- 地面阴影
    p.append(f'<ellipse cx="{cx}" cy="{floor}" rx="{sw*0.62:.0f}" ry="14" fill="#000000" opacity="0.4"/>')

    # --- 头部
    p.append(f'<ellipse cx="{cx-rx}" cy="{cy+14}" rx="10" ry="17" fill="{darken(skin,0.9)}"/>')
    p.append(f'<ellipse cx="{cx+rx}" cy="{cy+14}" rx="10" ry="17" fill="{darken(skin,0.9)}"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{skin}"/>')
    # 面部体积：双颊暗面 + 额头光
    p.append(f'<ellipse cx="{cx-rx*0.72:.0f}" cy="{cy+34}" rx="16" ry="34" fill="#000000" opacity="0.10"/>')
    p.append(f'<ellipse cx="{cx+rx*0.72:.0f}" cy="{cy+34}" rx="16" ry="34" fill="#000000" opacity="0.10"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy-46}" rx="{rx*0.6:.0f}" ry="26" fill="#FFFFFF" opacity="0.07"/>')

    # --- 胡须（画在五官下、嘴上）
    facial = c["hair"]["facial"]
    if facial == "stubble":
        p.append(f'<ellipse cx="{cx}" cy="{cy+ry*0.62:.0f}" rx="{rx*0.58:.0f}" ry="{ry*0.20:.0f}" fill="#241E1A" opacity="0.10"/>')
    elif facial in ("goatee", "thick_beard"):
        bw = rx * (0.92 if facial == "thick_beard" else 0.5)
        by = ry * (1.0 if facial == "thick_beard" else 0.72)
        p.append(f'<path d="M {cx-bw:.0f} {cy+ry*0.24:.0f} Q {cx} {cy+ry+by*0.5:.0f} {cx+bw:.0f} {cy+ry*0.24:.0f} '
                 f'Q {cx+bw*0.6:.0f} {cy+ry*0.62:.0f} {cx} {cy+ry*0.64:.0f} Q {cx-bw*0.6:.0f} {cy+ry*0.62:.0f} {cx-bw:.0f} {cy+ry*0.24:.0f} Z" '
                 f'fill="{darken(hair_hex,0.9)}"/>')
        if facial == "thick_beard":
            p.append(f'<path d="M {cx-bw*0.7:.0f} {cy+ry*0.14:.0f} Q {cx} {cy+ry*0.30:.0f} {cx+bw*0.7:.0f} {cy+ry*0.14:.0f} '
                     f'Q {cx+bw*0.5:.0f} {cy+ry*0.40:.0f} {cx} {cy+ry*0.40:.0f} Q {cx-bw*0.5:.0f} {cy+ry*0.40:.0f} {cx-bw*0.7:.0f} {cy+ry*0.14:.0f} Z" '
                     f'fill="{darken(hair_hex,0.9)}"/>')

    # --- 五官
    ey = cy - 10
    ex = 27
    for side in (-1, 1):
        x = cx + side * ex
        iris = darken(eye_hex, 0.9)
        if c["id"] == "tyrion-lannister":  # 异色瞳
            iris = "#3E5C46" if side == -1 else "#26201C"
        p.append(f'<path d="M {x-16} {ey} Q {x} {ey-11} {x+16} {ey} Q {x} {ey+9} {x-16} {ey} Z" fill="#F2EDE4"/>')
        p.append(f'<circle cx="{x}" cy="{ey-1}" r="7" fill="{iris}"/>')
        p.append(f'<circle cx="{x}" cy="{ey-1}" r="3.2" fill="#14100E"/>')
        p.append(f'<circle cx="{x-2}" cy="{ey-4}" r="1.7" fill="#FFFFFF" opacity="0.85"/>')
        p.append(f'<path d="M {x-16} {ey} Q {x} {ey-11} {x+16} {ey}" fill="none" stroke="#241E1A" stroke-width="2.4" stroke-opacity="0.75"/>')
        # 眉
        tilt = 6 if c["face"]["mouth"] in ("firm", "frown") else 2
        p.append(f'<path d="M {x-17} {ey-16+side*0+tilt} Q {x} {ey-24} {x+17} {ey-18}" fill="none" '
                 f'stroke="{darken(hair_hex,0.8)}" stroke-width="6.5" stroke-linecap="round"/>')
    # 鼻
    nw = 4.5 if c["id"] in ("robert-baratheon", "khal-drogo", "tyrion-lannister") else 3.4
    p.append(f'<path d="M {cx} {cy-2} L {cx-5} {cy+34} Q {cx} {cy+42} {cx+5} {cy+34}" fill="none" stroke="#000000" stroke-opacity="0.30" stroke-width="{nw}" stroke-linecap="round"/>')
    p.append(f'<circle cx="{cx-9}" cy="{cy+38}" r="2.6" fill="#000000" opacity="0.30"/>')
    p.append(f'<circle cx="{cx+9}" cy="{cy+38}" r="2.6" fill="#000000" opacity="0.30"/>')
    # 嘴
    my = cy + 62
    m = c["face"]["mouth"]
    d = {"neutral": f"M {cx-18} {my} Q {cx} {my+3} {cx+18} {my}",
         "firm":    f"M {cx-19} {my+2} Q {cx} {my-1} {cx+19} {my+2}",
         "smirk":   f"M {cx-17} {my+2} Q {cx+2} {my+4} {cx+19} {my-3}",
         "frown":   f"M {cx-17} {my+4} Q {cx} {my-2} {cx+17} {my+4}"}[m]
    p.append(f'<path d="{d}" fill="none" stroke="#7A4A3A" stroke-width="4.4" stroke-linecap="round"/>')
    p.append(f'<path d="M {cx-12} {my+10} Q {cx} {my+13} {cx+12} {my+10}" fill="none" stroke="#000000" stroke-opacity="0.22" stroke-width="3"/>')

    # --- 前层头发
    cap_top = cy - ry - 4
    if c["id"] == "jon-snow":
        p.append(f'<path d="M {cx-rx} {cy-6} Q {cx-rx} {cap_top-10} {cx} {cap_top-6} Q {cx+rx} {cap_top-10} {cx+rx} {cy-6} '
                 f'Q {cx+34} {cy-34} {cx} {cy-26} Q {cx-30} {cy-20} {cx-rx} {cy-6} Z" fill="{hair_hex}"/>')
        p.append(f'<path d="M {cx-rx} {cy-4} Q {cx-rx-6} {cy+30} {cx-rx+10} {cy+44} Q {cx-rx-2} {cy+10} {cx-rx+14} {cy-8} Z" fill="{hair_hex}"/>')
        p.append(f'<path d="M {cx+rx} {cy-4} Q {cx+rx+6} {cy+30} {cx+rx-10} {cy+44} Q {cx+rx+2} {cy+10} {cx+rx-14} {cy-8} Z" fill="{hair_hex}"/>')
    elif c["id"] == "khal-drogo":
        p.append(f'<path d="M {cx-rx-2} {cy-10} Q {cx-rx} {cap_top-8} {cx} {cap_top-4} Q {cx+rx} {cap_top-8} {cx+rx+2} {cy-10} '
                 f'Q {cx+rx} {cy-38} {cx} {cap_top+8} Q {cx-rx} {cy-38} {cx-rx-2} {cy-10} Z" fill="{hair_hex}"/>')
        p.append(f'<path d="M {cx+rx+2} {cy-6} C {cx+rx+26} {cy+40} {cx+rx+20} {cy+120} {cx+rx+30} 520" '
                 f'fill="none" stroke="{hair_hex}" stroke-width="14" stroke-linecap="round"/>')
        for i, dy in enumerate((10, 44, 80)):
            p.append(f'<circle cx="{cx+rx+ (18+i*4)}" cy="{cy+dy}" r="5" fill="{pal[2]["hex"]}"/>')
    elif c["id"] == "tyrion-lannister":
        p.append(f'<path d="M {cx-rx-4} {cy-2} Q {cx-rx-4} {cap_top-14} {cx} {cap_top-8} Q {cx+rx+4} {cap_top-14} {cx+rx+4} {cy-2} '
                 f'Q {cx+rx*0.5:.0f} {cy-30} {cx+6} {cy-16} Q {cx-20} {cy-4} {cx-rx*0.55:.0f} {cy-22} Q {cx-rx-2} {cy-14} {cx-rx-4} {cy-2} Z" '
                 f'fill="{hair_hex}"/>')
    else:
        p.append(f'<path d="M {cx-rx-2} {cy-12} Q {cx-rx-2} {cap_top-10} {cx} {cap_top-6} Q {cx+rx+2} {cap_top-10} {cx+rx+2} {cy-12} '
                 f'Q {cx+rx+2} {cy-40} {cx} {cap_top+10} Q {cx-rx-2} {cy-40} {cx-rx-2} {cy-12} Z" fill="{hair_hex}"/>')
        if c["hair"]["length"] != "short":
            p.append(f'<path d="M {cx-rx} {cy-8} Q {cx-rx-8} {cy+26} {cx-rx+8} {cy+40} L {cx-rx+14} {cy} Z" fill="{darken(hair_hex,0.9)}"/>')
            p.append(f'<path d="M {cx+rx} {cy-8} Q {cx+rx+8} {cy+26} {cx+rx-8} {cy+40} L {cx+rx-14} {cy} Z" fill="{hair_hex}"/>')

    # 提利昂鼻疤
    if c["id"] == "tyrion-lannister":
        p.append(f'<path d="M {cx-4} {cy+26} L {cx+6} {cy+34}" stroke="#8A5A48" stroke-width="2"/>')

    return "\n".join(p)


# ------------------------------------------------------------- silhouette --
def silhouette_svg(c):
    """底部剪影带：简化站姿 + 头身标尺。"""
    h_cm = c["build"]["height_cm"]
    ratio = c["build"]["head_ratio"]
    max_h = 118
    unit = max_h / ratio
    is_child = c["id"] in ("arya-stark", "bran-stark", "sansa-stark", "joffrey-baratheon")
    is_dress = c["id"] in ("catelyn-stark", "sansa-stark", "daenerys-targaryen", "cersei-lannister")
    body_h = unit * ratio
    hr = unit * 0.44
    cx = 300
    top = 990 + (max_h - body_h)  # 顶部对齐 max_h
    p = []
    fill = "#0A0B0D"
    p.append(f'<circle cx="{cx}" cy="{top+hr:.0f}" r="{hr:.0f}" fill="{fill}"/>')
    neck_y = top + hr * 2
    sw = unit * (2.6 if c["id"] in ("robert-baratheon", "khal-drogo") else 2.1)
    p.append(f'<rect x="{cx-6:.0f}" y="{neck_y:.0f}" width="12" height="{unit*0.35:.0f}" fill="{fill}"/>')
    if is_dress:
        p.append(f'<path d="M {cx-sw/2:.0f} {neck_y+unit*0.3:.0f} L {cx-sw*0.34:.0f} {top+body_h*0.52:.0f} '
                 f'L {cx-sw*0.95:.0f} {top+body_h:.0f} L {cx+sw*0.95:.0f} {top+body_h:.0f} '
                 f'L {cx+sw*0.34:.0f} {top+body_h*0.52:.0f} L {cx+sw/2:.0f} {neck_y+unit*0.3:.0f} Z" fill="{fill}"/>')
    else:
        p.append(f'<path d="M {cx-sw/2:.0f} {neck_y+unit*0.28:.0f} Q {cx} {neck_y+unit*0.1:.0f} {cx+sw/2:.0f} {neck_y+unit*0.28:.0f} '
                 f'L {cx+sw*0.42:.0f} {top+body_h*0.62:.0f} L {cx-sw*0.42:.0f} {top+body_h*0.62:.0f} Z" fill="{fill}"/>')
        leg_y = top + body_h * 0.60
        p.append(f'<rect x="{cx-10:.0f}" y="{leg_y:.0f}" width="8.5" height="{body_h*0.40:.0f}" fill="{fill}"/>')
        p.append(f'<rect x="{cx+2:.0f}" y="{leg_y:.0f}" width="8.5" height="{body_h*0.40:.0f}" fill="{fill}"/>')
    # 标尺
    rx0 = 400
    p.append(f'<line x1="{rx0}" y1="{top:.0f}" x2="{rx0}" y2="{top+max_h:.0f}" stroke="#4A4F55" stroke-width="2"/>')
    for i in range(int(ratio) + 1):
        y = top + i * unit
        tick = 10 if i % 2 == 0 else 6
        p.append(f'<line x1="{rx0}" y1="{y:.0f}" x2="{rx0+tick}" y2="{y:.0f}" stroke="#4A4F55" stroke-width="1.5"/>')
    p.append(f'<text x="{rx0+18}" y="{top+34:.0f}" font-family={FONT!r} font-size="14" fill="#B8BDC2">≈ {h_cm} cm</text>')
    p.append(f'<text x="{rx0+18}" y="{top+58:.0f}" font-family={FONT!r} font-size="14" fill="#B8BDC2">{ratio} 头身</text>')
    if is_child:
        p.append(f'<text x="{rx0+18}" y="{top+82:.0f}" font-family={FONT!r} font-size="12" fill="#8A8F94">未成年人比例</text>')
    # 道具
    props = "、".join(c.get("props", []))
    lines = wrap("道具 PROPS：" + props, 20)
    for i, ln in enumerate(lines):
        p.append(f'<text x="540" y="{top+22+i*24:.0f}" font-family={FONT!r} font-size="14" fill="#C8CCD0">{esc(ln)}</text>')
    return "\n".join(p)


# ------------------------------------------------------------------- page --
def sheet_svg(c, roster_version):
    pal_rows = []
    y0 = 196
    for i, pal in enumerate(c["palette"]):
        y = y0 + i * 62
        pal_rows.append(
            f'<rect x="596" y="{y}" width="46" height="46" rx="7" fill="{pal["hex"]}" stroke="#3A3E44"/>'
            f'<text x="656" y="{y+20}" font-family={FONT!r} font-size="14" fill="#E4E1DA">{esc(pal["name"])}</text>'
            f'<text x="656" y="{y+38}" font-family={FONT_MONO!r} font-size="13" fill="#8A8F94">{pal["hex"].upper()}</text>'
        )
    pal_end = y0 + 5 * 62

    def section(title, lines, y):
        out = [f'<text x="596" y="{y}" font-family={FONT!r} font-size="13" font-weight="bold" fill="#8A8F94" letter-spacing="3">{esc(title)}</text>']
        yy = y + 24
        for ln in lines:
            out.append(f'<text x="596" y="{yy}" font-family={FONT!r} font-size="13.5" fill="#C8CCD0">{esc(ln)}</text>')
            yy += 21
        return "\n".join(out), yy

    feat_lines = []
    for f in c["features"]:
        feat_lines.extend(wrap("· " + f, 16))
    sec1, y1 = section("标志特征 FEATURES", feat_lines, pal_end + 36)
    sec2, y2 = section("服装 COSTUME", wrap(c["costume"], 16), y1 + 40)
    sec3, y3 = section("气质 DEMEANOR", wrap(c["demeanor"], 16), y2 + 40)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="torsoShade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000000" stop-opacity="0.30"/>
    <stop offset="0.45" stop-color="#000000" stop-opacity="0.02"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.06"/>
  </linearGradient>
  <radialGradient id="vignette" cx="0.5" cy="0.42" r="0.95">
    <stop offset="0.62" stop-color="#1E2126" stop-opacity="0"/>
    <stop offset="1" stop-color="#0D0E10" stop-opacity="0.9"/>
  </radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="#181B1F"/>
<rect width="{W}" height="{H}" fill="url(#vignette)"/>

<rect x="40" y="36" width="7" height="66" fill="{c["house_color"]}"/>
<text x="62" y="72" font-family={FONT!r} font-size="38" font-weight="bold" fill="#EDEAE2">{esc(c["name_zh"])}</text>
<text x="63" y="100" font-family={FONT!r} font-size="16" fill="#9BA0A4">{esc(c["name_en"])}</text>
<text x="860" y="62" text-anchor="end" font-family={FONT!r} font-size="15" fill="#C8CCD0">{esc(c["role"])}</text>
<text x="860" y="88" text-anchor="end" font-family={FONT!r} font-size="13" fill="#8A8F94">{esc(c["house"])} · 首秀 {c["first_episode"]} · 设计 v{c["design_version"]}</text>
<line x1="40" y1="122" x2="860" y2="122" stroke="#2E3236" stroke-width="2"/>

<rect x="50" y="146" width="500" height="816" rx="12" fill="#1B1E22" stroke="#2E3236"/>
<text x="70" y="180" font-family={FONT!r} font-size="13" font-weight="bold" fill="#8A8F94" letter-spacing="3">正面设定 FRONT VIEW</text>
{portrait_svg(c)}

{"".join(pal_rows)}
{sec1}
{sec2}
{sec3}

<rect x="50" y="982" width="810" height="166" rx="12" fill="#1B1E22" stroke="#2E3236"/>
<text x="70" y="1012" font-family={FONT!r} font-size="13" font-weight="bold" fill="#8A8F94" letter-spacing="3">剪影与比例 SILHOUETTE</text>
{silhouette_svg(c)}

<text x="40" y="1178" font-family={FONT!r} font-size="11.5" fill="#6E7378">美漫厚涂 · 参考《双城之战》｜视觉标准见 bible/style-guide.md</text>
<text x="860" y="1178" text-anchor="end" font-family={FONT!r} font-size="11.5" fill="#6E7378">生成物勿手改 · 改 roster.json 后重跑 tools/gen_character_sheet.py · roster v{roster_version}</text>
</svg>
'''


# -------------------------------------------------------------- design.md --
AUTO_BEGIN = "<!-- AUTO:BEGIN（本区由生成器维护，勿手改） -->"
AUTO_END = "<!-- AUTO:END -->"


def design_md(c, roster_version):
    pal = "\n".join(f"| {p['name']} | `{p['hex'].upper()}` |" for p in c["palette"])
    feat = "\n".join(f"- {f}" for f in c["features"])
    props = "、".join(c.get("props", []))
    b, f_, h = c["build"], c["face"], c["hair"]
    body = f"""# {c['name_zh']}（{c['name_en']}）角色设计

{AUTO_BEGIN}
## 基本信息

| 项 | 内容 |
|----|------|
| character-id | `{c['id']}` |
| 家族 / 势力 | {c['house']}（家族色 `{c['house_color'].upper()}`） |
| 定位 | {c['role']} |
| 年龄观感 | {c['age_look']} |
| 首秀集 | {c['first_episode']} |
| 设计版本 | v{c['design_version']}（roster v{roster_version}） |

## 体型

- 身高 ≈ {b['height_cm']} cm，{b['head_ratio']} 头身
- 体型：{b['body_type']}

## 面容

- 脸型：{f_['shape']} ｜ 肤色 `{f_['skin_hex'].upper()}` ｜ 瞳色 `{f_['eye_hex'].upper()}`（{f_['eye_desc']}）
- 鼻：{f_['nose']} ｜ 唇形基调：{f_['mouth']}
- 发：{h['desc']}（`{h['hex'].upper()}`，{h['length']}）｜ 胡须：{h['facial']}

## 服装

{c['costume']}

## 调色板（渲染 prompt 必须逐项引用）

| 用途 | HEX |
|------|-----|
{pal}

## 标志特征（质检对照项）

{feat}

## 标志道具

{props}
{AUTO_END}

## 气质与表演（手写区）

- 气质：{c['demeanor']}
- 声线：{c.get('voice', '待定')}
- 标志动作：{c.get('signature', '待定')}
- 角色弧线：{c.get('arc', '待定')}

## 渲染注意事项

- 关键帧 prompt 末尾附上表全部 HEX 与「标志特征」关键词，禁止凭记忆重述外观。
- 该角色与其他角色的同框区分度优先级：{c['name_zh']} 的发色与服装主色不得与对手戏角色撞色（详见 bible/style-guide.md §4）。

## 变更记录

| 日期 | 版本 | 变更 | 决策链接 |
|------|------|------|----------|
| 初始化 | v{c['design_version']} | 从 roster.json 首次生成 | — |
"""
    return body


# ------------------------------------------------------------------- main --
def main():
    data = json.loads(ROSTER.read_text(encoding="utf-8"))
    roster_version = data.get("version", 1)
    chars = data["characters"]
    only = set(sys.argv[1:])
    index_rows = ["| id | 中文名 | 定位 | 首秀 | 设计版本 |", "|----|--------|------|------|----------|"]
    made = 0
    for c in chars:
        validate(c)
        if only and c["id"] not in only:
            index_rows.append(f"| `{c['id']}` | {c['name_zh']} | {c['role']} | {c['first_episode']} | v{c['design_version']} |")
            continue
        cdir = OUT_DIR / c["id"]
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / "sheet.svg").write_text(sheet_svg(c, roster_version), encoding="utf-8")
        dpath = cdir / "design.md"
        auto_re = re.compile(re.escape(AUTO_BEGIN) + r".*?" + re.escape(AUTO_END), re.S)
        new_auto = auto_re.search(design_md(c, roster_version)).group(0)
        if dpath.exists():
            text = dpath.read_text(encoding="utf-8")
            if auto_re.search(text):
                dpath.write_text(auto_re.sub(lambda _: new_auto, text), encoding="utf-8")
            else:
                print(f"  跳过 {c['id']}/design.md（存在但无 AUTO 标记区）")
        else:
            dpath.write_text(design_md(c, roster_version), encoding="utf-8")
        index_rows.append(f"| `{c['id']}` | {c['name_zh']} | {c['role']} | {c['first_episode']} | v{c['design_version']} |")
        made += 1
        print(f"OK: characters/{c['id']}/  sheet.svg + design.md")
    if not only:
        (OUT_DIR / "_index.md").write_text(
            "# 角色总索引（由生成器自动维护）\n\n"
            f"共 {len(chars)} 个角色 ｜ roster.json v{roster_version} ｜ 生成器：tools/gen_character_sheet.py\n\n"
            + "\n".join(index_rows) + "\n",
            encoding="utf-8",
        )
        print(f"OK: characters/_index.md（{len(chars)} 角色）")
    print(f"完成：{made} 个角色的设定文件已生成")


if __name__ == "__main__":
    main()
