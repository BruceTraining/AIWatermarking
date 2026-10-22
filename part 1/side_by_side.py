"""DEMO 1, step 2: put the 2 photos side by side, and measure how different they are.

Usage:
    uv run python side_by_side.py

It reads input/original.jpg and output/watermarked.png, and it writes 3 files:
    output/side_by_side.png     the 2 photos in a random order (for the vote)
    output/answer.txt           which side carries the watermark
    output/difference_x20.png   the difference between the 2, made 20 times brighter
"""
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageOps

ORIGINAL = Path("input/original.jpg")
WATERMARKED = Path("output/watermarked.png")
OUT = Path("output")

if not ORIGINAL.is_file():
    sys.exit(f"I can't find {ORIGINAL.as_posix()}. Check the file name, "
             "or run make_test_image.py to make a test picture.")
if not WATERMARKED.is_file():
    sys.exit(f"I can't find {WATERMARKED.as_posix()}. Run tm_encode.py first.")

a = ImageOps.exif_transpose(Image.open(ORIGINAL)).convert("RGB")
b = Image.open(WATERMARKED).convert("RGB")
if a.size != b.size:
    sys.exit(f"The 2 photos have different sizes ({a.size} and {b.size}). "
             "Run tm_encode.py again on input/original.jpg.")

# How different are they? PSNR is the standard answer: a higher number is a smaller change.
x = np.asarray(a, dtype=np.float64)
y = np.asarray(b, dtype=np.float64)
mse = np.mean((x - y) ** 2)
psnr = 10 * np.log10(255.0 ** 2 / mse) if mse > 0 else float("inf")
print(f"PSNR:                        {psnr:.2f} dB")
print(f"largest single-pixel change: {int(np.abs(x - y).max())} of 255")
print(f"average pixel change:        {np.abs(x - y).mean():.2f} of 255")

# Side by side, in a random order, so that even the presenter has to read the answer.
pair = [("original", a), ("watermarked", b)]
random.shuffle(pair)
w, h = a.size
gap = 24
canvas = Image.new("RGB", (w * 2 + gap, h), "white")
canvas.paste(pair[0][1], (0, 0))
canvas.paste(pair[1][1], (w + gap, 0))
canvas.save(OUT / "side_by_side.png")
(OUT / "answer.txt").write_text(f"left = {pair[0][0]}, right = {pair[1][0]}\n")
print("saved output/side_by_side.png  (the answer is in output/answer.txt)")

# The hidden signal: multiply every pixel difference by 20, so that you can see it.
diff = ImageChops.difference(a, b).point(lambda v: min(255, v * 20))
diff.save(OUT / "difference_x20.png")
print("saved output/difference_x20.png")
