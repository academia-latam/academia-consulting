#!/usr/bin/env python3
"""
Key AcademIA's black-on-white illustrations to transparent PNGs.

The generator (gen-images.py) produces solid BLACK ink on a near-white paper
ground. This script removes the paper (white -> alpha) and recolors the ink to a
near-navy black so the art sits cleanly on the white sections AND, with a CSS
`filter: invert(1)`, becomes crisp white line-art on the electric-blue sections.

Reads  assets/img/<name>.png  ->  writes  assets/img/<name>-t.png

USAGE
    python tools/key-transparent.py icon-train hero-spark      # specific names
    python tools/key-transparent.py                            # all *.png missing a -t
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

INK = (16, 20, 36)        # near-navy black (elegant, not flat #000)
HI = 238                  # luminance >= HI  -> fully transparent (paper)
LO = 180                  # luminance <= LO  -> fully opaque ink
# in between -> antialiased edge ramp


def alpha_table():
    t = []
    for v in range(256):
        if v >= HI:
            t.append(0)
        elif v <= LO:
            t.append(255)
        else:
            t.append(int((HI - v) / (HI - LO) * 255))
    return t


def key(name):
    src = os.path.join(OUT, name + ".png")
    if not os.path.exists(src):
        print(f"- {name}: no source .png, skip")
        return False
    img = Image.open(src).convert("RGB")
    lum = img.convert("L")
    alpha = lum.point(alpha_table())
    out = Image.new("RGBA", img.size, INK + (0,))
    out.putalpha(alpha)
    out.save(os.path.join(OUT, name + "-t.png"))
    out.save(os.path.join(OUT, name + "-t.webp"), "WEBP", quality=88, method=6)
    print(f"  keyed assets/img/{name}-t.png + .webp ({img.size[0]}x{img.size[1]})")
    return True


def main():
    names = sys.argv[1:]
    if not names:
        names = sorted({f[:-4] for f in os.listdir(OUT)
                        if f.endswith(".png") and not f.endswith("-t.png")})
    n = sum(key(x) for x in names)
    print(f"\nDone: keyed {n} image(s).")


if __name__ == "__main__":
    main()
