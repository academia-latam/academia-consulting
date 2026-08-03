#!/usr/bin/env python3
"""Bake the duotone engravings used by catalogo-ilustrado.html into flat JPEGs.

Why bake instead of doing it in CSS: mix-blend-mode and mask-image force Chromium to
rasterise the entire plate when printing to PDF. The same brochure went from 852 KB to
16 MB with the CSS version. Baking the screen blend and the edge fade into the image
lets the PDF embed a plain JPEG.

Run from the repo root:  python3 tools/brochure/bake-etch.py
"""
from PIL import Image, ImageChops
import numpy as np
import pathlib

BASE = (11, 15, 61)          # --deep, #0b0f3d
OUT = pathlib.Path('tools/brochure/img')
SRC = pathlib.Path('assets/img')

# source, output, size at 150 dpi for the placed box, fade direction
JOBS = [
    ('etch-faust-neg.webp',  'faust.jpg',  (930, 1650), 'h'),   # .etch--r    6.2in x 11in
    ('teach-ostade.webp',    'ostade.jpg', (1275, 525), 'v'),   # .etch--band 8.5in x 3.5in
    ('etch-athens-pos.webp', 'athens.jpg', (930, 1650), 'h'),
]


def cover(im, w, h, vertical_anchor=0.36):
    """Crop to the target aspect ratio, then resize. Mirrors CSS object-fit: cover."""
    src_ratio, target_ratio = im.width / im.height, w / h
    if src_ratio > target_ratio:
        nw = int(im.height * target_ratio)
        im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
    else:
        nh = int(im.width / target_ratio)
        off = int((im.height - nh) * vertical_anchor)
        im = im.crop((0, off, im.width, off + nh))
    return im.resize((w, h), Image.LANCZOS)


def bake(src, dst, size, fade):
    w, h = size
    im = cover(Image.open(SRC / src).convert('RGB'), w, h)
    base = Image.new('RGB', (w, h), BASE)
    blended = ImageChops.screen(base, Image.blend(base, im, 0.62))

    a = np.asarray(blended).astype(np.float32)
    b = np.array(BASE, dtype=np.float32)
    if fade == 'h':      # fade in from the left edge, so the plate absorbs the image
        mask = np.clip((np.linspace(0, 1, w) - 0.04) / 0.46, 0, 1)[None, :, None]
    else:                # fade out at the bottom of the band
        mask = np.clip((1 - np.linspace(0, 1, h)) / 0.30, 0, 1)[:, None, None]

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / dst
    Image.fromarray((b + (a - b) * mask).astype(np.uint8)).save(
        path, quality=84, optimize=True, progressive=True)
    print(f'{dst:12} {w}x{h}  {path.stat().st_size // 1024} KB')


if __name__ == '__main__':
    for job in JOBS:
        bake(*job)
