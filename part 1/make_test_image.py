"""Optional: make a textured test photo when you don't have one of your own.

Usage:
    uv run python make_test_image.py

It writes input/original.jpg (1600 x 1000 pixels). A watermark hides in texture,
so this picture is noisy on purpose. A real photo is still the better choice.
"""
from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path("input/original.jpg")

rng = np.random.default_rng(7)          # a fixed seed, so everybody gets the same picture
h, w = 1000, 1600
y, x = np.mgrid[0:h, 0:w]
r = 128 + 100 * np.sin(x / 90.0) + rng.normal(0, 12, (h, w))
g = 128 + 100 * np.cos(y / 70.0) + rng.normal(0, 12, (h, w))
b = 128 + 60 * np.sin((x + y) / 120.0) + rng.normal(0, 12, (h, w))
img = np.stack([r, g, b], axis=-1).clip(0, 255).astype(np.uint8)

OUT.parent.mkdir(exist_ok=True)
Image.fromarray(img).save(OUT, quality=95)
print(f"saved {OUT.as_posix()}  ({w} x {h} pixels)")
