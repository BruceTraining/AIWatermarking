"""DEMO 2, step 1: ask TrustMark whether a picture carries a watermark.

Usage:
    uv run python tm_decode.py input/original.jpg output/watermarked.png
    uv run python tm_decode.py path/to/a_screenshot.png

The detector needs nothing but the picture. It doesn't need the original photo.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError
from trustmark import TrustMark

BCH_5 = 1    # the number of the error-correction scheme that tm_encode.py uses (TrustMark's default)

paths = [Path(p) for p in sys.argv[1:]]
if not paths:
    sys.exit("Give me at least 1 picture, for example:\n"
             "    uv run python tm_decode.py input/original.jpg output/watermarked.png")

tm = TrustMark(model_type="Q", verbose=False, loadRemover=False)
if tm.decoder is None:
    sys.exit("TrustMark could not load its model files. "
             "See 'If the Model Download Fails' in README.md.")

for path in paths:
    if not path.is_file():
        print(f"{path.as_posix():34s} file not found")
        continue
    try:
        img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    except UnidentifiedImageError:
        print(f"{path.as_posix():34s} isn't a picture that I can open")
        continue
    secret, present, scheme = tm.decode(img)
    # "present" is True only when the error-correction check passes, so this is a yes or a no.
    # We also insist on our own scheme, which makes a false "yes" on random pixels about 50 times rarer.
    if present and scheme == BCH_5:
        print(f"{path.as_posix():34s} WATERMARK FOUND   payload={secret!r}")
    else:
        print(f"{path.as_posix():34s} no watermark")
