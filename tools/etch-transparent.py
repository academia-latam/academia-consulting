#!/usr/bin/env python3
"""
Key a public-domain etching/print (dark ink on light paper) into a TRANSPARENT
ink illustration: paper -> alpha, ink -> near-navy. Sits as contained line-art
on the white/surface sections (and inverts to white on blue with filter:invert).

Handles JPEG/PNG/TIFF sources (Pillow opens by content). Autocontrasts first so
aged/cream paper still keys to clean transparency.

USAGE
    python tools/etch-transparent.py SRC OUT_BASE [--lo 120 --hi 205] [--crop-box l,t,r,b]
    -> writes OUT_BASE.png and OUT_BASE.webp
"""
import argparse, sys
from PIL import Image, ImageOps

INK = (16, 20, 36)  # near-navy black, matches key-transparent.py


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")  # base path, no extension
    ap.add_argument("--lo", type=int, default=120, help="L <= lo -> fully opaque ink")
    ap.add_argument("--hi", type=int, default=205, help="L >= hi -> fully transparent paper")
    ap.add_argument("--crop-box", default="")
    ap.add_argument("--maxpx", type=int, default=1500, help="downscale longest side to this before saving")
    a = ap.parse_args()

    try:
        img = Image.open(a.src).convert("RGB")
    except Exception as e:
        print(f"ERROR opening {a.src}: {e}")
        sys.exit(1)
    if a.crop_box:
        l, t, r, b = (float(x) for x in a.crop_box.split(","))
        W, H = img.size
        img = img.crop((int(l * W), int(t * H), int(r * W), int(b * H)))

    lum = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    lo, hi = a.lo, a.hi
    table = []
    for v in range(256):
        if v >= hi:
            table.append(0)
        elif v <= lo:
            table.append(255)
        else:
            table.append(int((hi - v) / (hi - lo) * 255))
    alpha = lum.point(table)
    out = Image.new("RGBA", img.size, INK + (0,))
    out.putalpha(alpha)
    if max(out.size) > a.maxpx:
        out.thumbnail((a.maxpx, a.maxpx), Image.LANCZOS)
    out.save(a.out + ".png")
    out.save(a.out + ".webp", "WEBP", quality=88, method=4)
    print(f"  keyed {a.out}.png + .webp ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
