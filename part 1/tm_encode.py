"""DEMO 1, step 1: hide 8 characters in a photo with TrustMark.

Usage:
    uv run python tm_encode.py                          # input/original.jpg, payload ORLY2026
    uv run python tm_encode.py input/my_photo.jpg HELLO # your own photo and payload

It writes output/watermarked.png. The first run also downloads 3 model files.
"""
import sys
import time
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError
from trustmark import TrustMark

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input/original.jpg")
PAYLOAD = sys.argv[2] if len(sys.argv) > 2 else "ORLY2026"
OUT = Path("output/watermarked.png")

if not SRC.is_file():
    sys.exit(f"I can't find {SRC.as_posix()}. Check the file name, "
             "or run make_test_image.py to make a test picture.")
if len(PAYLOAD) > 8 or not PAYLOAD.isascii():
    sys.exit("The payload holds 8 plain ASCII characters at most, for example ORLY2026.")

# Model Q is TrustMark's default. We never remove a watermark, so we skip that model.
tm = TrustMark(model_type="Q", verbose=False, loadRemover=False)
if tm.encoder is None or tm.decoder is None:
    sys.exit("TrustMark could not load its model files. "
             "See 'If the Model Download Fails' in README.md.")

# exif_transpose turns a phone photo the right way up before we touch the pixels.
try:
    cover = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
except UnidentifiedImageError:
    sys.exit(f"{SRC.as_posix()} isn't a picture that I can open. "
             "An iPhone HEIC photo has to be exported as a JPEG first.")

start = time.time()
stego = tm.encode(cover, PAYLOAD)
seconds = time.time() - start

OUT.parent.mkdir(exist_ok=True)
stego.save(OUT)                      # PNG keeps every pixel value exactly as it is
print(f"photo:    {SRC.as_posix()}  ({cover.width} x {cover.height} pixels)")
print(f"payload:  {PAYLOAD!r}")
print(f"encoded in {seconds:.2f} seconds")
print(f"saved:    {OUT.as_posix()}")
