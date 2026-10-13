#!/usr/bin/env python3
"""Legalwithdigvijay carousel renderer.

Usage: python3 render.py post.json OUT_DIR
Writes 01.jpg, 02.jpg ... (1080x1350, JPEG) into OUT_DIR.

post.json:
{
  "slides": [
    {"type": "cover", "kicker": "...", "title": "...", "subtitle": "...", "cite": "..."},
    {"type": "content", "label": "...", "title": "...", "bullets": ["..."], "note": "..."},
    {"type": "cta", "title": "...", "lines": ["..."]}
  ]
}
Inline **text** is drawn in brass/bold for emphasis.
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
M = 84  # side margin
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")

BG = (14, 38, 31)          # deep green
BG2 = (20, 52, 42)         # panel green
BRASS = (201, 164, 92)
CREAM = (243, 235, 221)
MUTED = (170, 186, 176)
INK = (14, 38, 31)

def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

SERIF_XB = "playfair-display-latin-800-normal.woff"
SERIF_B = "playfair-display-latin-700-normal.woff"
SERIF_I = "playfair-display-latin-700-italic.woff"
SANS = "Inter-Regular.otf"
SANS_M = "Inter-Medium.otf"
SANS_SB = "Inter-SemiBold.otf"
SANS_B = "Inter-Bold.otf"
SANS_XB = "Inter-ExtraBold.otf"


def runs(text):
    """Split text into words; each word is a list of (segment, emphasised).
    ** toggles emphasis and may sit inside a word, so punctuation stays attached."""
    words, cur, emph = [], [], False
    for i, part in enumerate(re.split(r"(\*\*)", text)):
        if part == "**":
            emph = not emph
            continue
        chunks = part.split(" ")
        for j, c in enumerate(chunks):
            if j > 0:
                if cur:
                    words.append(cur)
                cur = []
            if c:
                cur.append((c, emph))
    if cur:
        words.append(cur)
    return words


def wlen(draw, word, font, efont):
    return sum(draw.textlength(s, font=efont if e else font) for s, e in word)


def wrap(draw, text, font, efont, maxw):
    lines, line, lw = [], [], 0
    space = draw.textlength(" ", font=font)
    for w in runs(text):
        ww = wlen(draw, w, font, efont)
        add = ww + (space if line else 0)
        if line and lw + add > maxw:
            lines.append(line)
            line, lw = [w], ww
        else:
            line.append(w)
            lw += add
    if line:
        lines.append(line)
    return lines


def draw_rich(draw, xy, text, font, efont, maxw, color, ecolor, lh):
    x0, y = xy
    space = draw.textlength(" ", font=font)
    for line in wrap(draw, text, font, efont, maxw):
        x = x0
        for w in line:
            for s, e in w:
                f = efont if e else font
                draw.text((x, y), s, font=f, fill=ecolor if e else color)
                x += draw.textlength(s, font=f)
            x += space
        y += lh
    return y


def text_height(draw, text, font, efont, maxw, lh):
    return len(wrap(draw, text, font, efont, maxw)) * lh


def frame(img, idx, total):
    d = ImageDraw.Draw(img)
    # thin brass frame
    d.rectangle([36, 36, W - 37, H - 37], outline=(*BRASS,), width=2)
    # header
    d.text((M, 70), "LEGALWITHDIGVIJAY", font=F(SANS_B, 24), fill=BRASS)
    t = f"{idx}/{total}"
    tw = d.textlength(t, font=F(SANS_SB, 24))
    d.text((W - M - tw, 70), t, font=F(SANS_SB, 24), fill=MUTED)
    d.line([M, 112, W - M, 112], fill=(60, 90, 78), width=1)
    # footer
    d.line([M, H - 118, W - M, H - 118], fill=(60, 90, 78), width=1)
    d.text((M, H - 98), "Adv. Digvijay Singh  ·  Allahabad High Court, Lucknow Bench",
           font=F(SANS_M, 22), fill=MUTED)
    if idx < total:
        s = "Swipe  →"
        sw = d.textlength(s, font=F(SANS_B, 24))
        d.text((W - M - sw, H - 99), s, font=F(SANS_B, 24), fill=BRASS)
    return d


def cover(s, idx, total):
    img = Image.new("RGB", (W, H), BG)
    d = frame(img, idx, total)
    maxw = W - 2 * M
    y = 270
    # kicker pill
    k = s.get("kicker", "").upper()
    kf = F(SANS_B, 26)
    kw = d.textlength(k, font=kf)
    d.rounded_rectangle([M, y, M + kw + 44, y + 54], radius=27, fill=BRASS)
    d.text((M + 22, y + 12), k, font=kf, fill=INK)
    y += 110
    # headline
    tf, tfe = F(SERIF_XB, 92), F(SERIF_I, 92)
    y = draw_rich(d, (M, y), s["title"], tf, tfe, maxw, CREAM, BRASS, 108)
    y += 30
    d.rectangle([M, y, M + 120, y + 6], fill=BRASS)
    y += 50
    if s.get("subtitle"):
        y = draw_rich(d, (M, y), s["subtitle"], F(SANS_M, 38), F(SANS_B, 38), maxw, CREAM, BRASS, 54)
    # citation block at bottom
    if s.get("cite"):
        cf = F(SANS, 26)
        ch = text_height(d, s["cite"], cf, cf, maxw - 48, 38)
        top = H - 160 - ch - 40
        d.rectangle([M, top, M + 6, top + ch + 16], fill=BRASS)
        draw_rich(d, (M + 30, top + 6), s["cite"], cf, F(SANS_SB, 26), maxw - 48, MUTED, CREAM, 38)
    return img


def content(s, idx, total):
    img = Image.new("RGB", (W, H), BG)
    d = frame(img, idx, total)
    maxw = W - 2 * M
    y = 170
    if s.get("label"):
        d.text((M, y), s["label"].upper(), font=F(SANS_B, 26), fill=BRASS)
        y += 56
    y = draw_rich(d, (M, y), s["title"], F(SERIF_XB, 64), F(SERIF_I, 64), maxw, CREAM, BRASS, 78)
    y += 44
    bf, bfe = F(SANS, 36), F(SANS_B, 36)
    for b in s.get("bullets", []):
        d.rectangle([M, y + 18, M + 14, y + 32], fill=BRASS)
        y = draw_rich(d, (M + 40, y), b, bf, bfe, maxw - 40, CREAM, BRASS, 52)
        y += 26
    if s.get("note"):
        nf, nfe = F(SANS_SB, 34), F(SANS_XB, 34)
        nh = text_height(d, s["note"], nf, nfe, maxw - 72, 48)
        top = max(y + 20, H - 160 - nh - 60)
        d.rounded_rectangle([M, top, W - M, top + nh + 56], radius=18, fill=BG2, outline=BRASS, width=2)
        draw_rich(d, (M + 36, top + 26), s["note"], nf, nfe, maxw - 72, CREAM, BRASS, 48)
    return img


def cta(s, idx, total):
    img = Image.new("RGB", (W, H), BG)
    d = frame(img, idx, total)
    maxw = W - 2 * M
    y = 300
    y = draw_rich(d, (M, y), s["title"], F(SERIF_XB, 80), F(SERIF_I, 80), maxw, CREAM, BRASS, 96)
    y += 40
    d.rectangle([M, y, M + 120, y + 6], fill=BRASS)
    y += 60
    for ln in s.get("lines", []):
        y = draw_rich(d, (M, y), ln, F(SANS_M, 38), F(SANS_B, 38), maxw, CREAM, BRASS, 54)
        y += 18
    h = "@legalwithdigvijay"
    hf = F(SANS_XB, 48)
    hw = d.textlength(h, font=hf)
    top = H - 330
    d.rounded_rectangle([M, top, M + hw + 70, top + 90], radius=45, fill=BRASS)
    d.text((M + 35, top + 18), h, font=hf, fill=INK)
    return img


def main(src, out):
    post = json.load(open(src, encoding="utf-8"))
    os.makedirs(out, exist_ok=True)
    slides = post["slides"]
    n = len(slides)
    paths = []
    for i, s in enumerate(slides, 1):
        img = {"cover": cover, "content": content, "cta": cta}[s["type"]](s, i, n)
        p = os.path.join(out, f"{i:02d}.jpg")
        img.save(p, "JPEG", quality=90, optimize=True, progressive=False)
        paths.append(p)
    print("\n".join(paths))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
