"""DEMO 2, step 2: edit the watermarked photo, and check whether the watermark survives.

Usage:
    uv run python tm_edits.py

It reads output/watermarked.png, saves every edited copy as output/edit_<name>.png,
and prints FOUND or LOST for each one.
"""
import io
import sys
from pathlib import Path

from PIL import Image
from trustmark import TrustMark

WATERMARKED = Path("output/watermarked.png")
OUT = Path("output")
BCH_5 = 1    # the number of the error-correction scheme that tm_encode.py uses (TrustMark's default)

if not WATERMARKED.is_file():
    sys.exit(f"I can't find {WATERMARKED.as_posix()}. Run tm_encode.py first.")

tm = TrustMark(model_type="Q", verbose=False, loadRemover=False)
if tm.decoder is None:
    sys.exit("TrustMark could not load its model files. "
             "See 'If the Model Download Fails' in README.md.")

wm = Image.open(WATERMARKED).convert("RGB")
w, h = wm.size

# Read the hidden text from the untouched copy first, so that we know what to look for.
hidden, present, scheme = tm.decode(wm)
if not (present and scheme == BCH_5):
    sys.exit(f"I can't find a watermark in {WATERMARKED.as_posix()}. Run tm_encode.py again.")


def jpeg(img, quality):
    """Save the picture as a JPEG in memory, and open it again."""
    buffer = io.BytesIO()
    img.save(buffer, "JPEG", quality=quality)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def crop(img, margin):
    """Cut the same share off all 4 sides. A margin of 0.20 cuts 20% off every side."""
    iw, ih = img.size
    return img.crop((int(iw * margin), int(ih * margin),
                     int(iw * (1 - margin)), int(ih * (1 - margin))))


edits = {
  "jpeg_q85":     jpeg(wm, 85),
  "jpeg_q50":     jpeg(wm, 50),
  "resize_50pct": wm.resize((w // 2, h // 2)),
  "resize_25pct": wm.resize((w // 4, h // 4)),
  "crop_10pct":   crop(wm, 0.05),
  "crop_40pct":   crop(wm, 0.20),
}

print(f"{'edit':14s} {'size':>13s}   result")
for name, img in edits.items():
    img.save(OUT / f"edit_{name}.png")
    secret, present, scheme = tm.decode(img)
    size = f"{img.width} x {img.height}"
    # FOUND means that the same text came back. Anything else counts as LOST.
    if present and scheme == BCH_5 and secret == hidden:
        result = f"FOUND   payload={secret!r}"
    else:
        result = "LOST"
    print(f"{name:14s} {size:>13s}   {result}")
