#!/usr/bin/env python3
"""
Bake a public-domain etching/engraving into an AcademIA duotone hero image.

Etchings are line art (dark ink on light paper). For a dramatic hero that sits
behind white text, we want a DEEP NAVY field with the engraving GLOWING in
electric blue / near-white on the right (mode=glow). An alternate ink mode keeps
the classic light-paper / dark-drawing look.

The duotone is baked into the file, so the hero <img> needs NO mix-blend-mode
(use the `.duo-bg--baked` class which sets blend:normal, filter:none).

USAGE
    python tools/duotone-hero.py SRC OUT [--w 1800 --h 1100]
        [--mode glow|ink] [--cx 0.5 --cy 0.4] [--gamma 1.0] [--contrast 1.0]
        [--shadow 7,9,30] [--highlight 150,180,255]
"""
import argparse, sys
from PIL import Image, ImageOps, ImageEnhance


def parse_rgb(s):
    return tuple(int(x) for x in s.split(","))


def duotone(lum, shadow, highlight, mode, gamma):
    # lum: 8-bit L image. t in [0,1] drives shadow->highlight.
    # glow: paper(bright)->shadow(navy), ink(dark)->highlight(electric)
    # ink:  paper(bright)->highlight(light), ink(dark)->shadow(navy)
    lut_r, lut_g, lut_b = [], [], []
    for v in range(256):
        n = v / 255.0
        t = (1.0 - n) if mode == "glow" else n
        if gamma != 1.0:
            t = t ** gamma
        lut_r.append(int(round(shadow[0] + (highlight[0] - shadow[0]) * t)))
        lut_g.append(int(round(shadow[1] + (highlight[1] - shadow[1]) * t)))
        lut_b.append(int(round(shadow[2] + (highlight[2] - shadow[2]) * t)))
    r = lum.point(lut_r)
    g = lum.point(lut_g)
    b = lum.point(lut_b)
    return Image.merge("RGB", (r, g, b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--w", type=int, default=1800)
    ap.add_argument("--h", type=int, default=1100)
    ap.add_argument("--mode", choices=["glow", "ink"], default="glow")
    ap.add_argument("--cx", type=float, default=0.5)
    ap.add_argument("--cy", type=float, default=0.42)
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--contrast", type=float, default=1.08)
    ap.add_argument("--shadow", default="7,9,30")
    ap.add_argument("--highlight", default="150,180,255")
    ap.add_argument("--crop-box", default="", help="pre-crop as fractions left,top,right,bottom (0-1) to zoom in before fitting")
    a = ap.parse_args()

    try:
        img = Image.open(a.src)
    except Exception as e:
        print(f"ERROR opening {a.src}: {e}")
        sys.exit(1)
    img = img.convert("RGB")
    if a.crop_box:
        l, t, r, btm = (float(x) for x in a.crop_box.split(","))
        W, H = img.size
        img = img.crop((int(l * W), int(t * H), int(r * W), int(btm * H)))
    lum = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    if a.contrast != 1.0:
        lum = ImageEnhance.Contrast(lum).enhance(a.contrast)
    duo = duotone(lum, parse_rgb(a.shadow), parse_rgb(a.highlight), a.mode, a.gamma)
    duo = ImageOps.fit(duo, (a.w, a.h), Image.LANCZOS, centering=(a.cx, a.cy))
    duo.save(a.out, "WEBP", quality=86, method=6)
    print(f"  saved {a.out} ({a.w}x{a.h}) mode={a.mode}")


if __name__ == "__main__":
    main()
