"""Only if the model download fails: copy TrustMark's model files in by hand.

Usage:
    uv run python copy_models.py path/to/the/folder/with/the/3/files

The folder must hold trustmark_Q.yaml, encoder_Q.ckpt, and decoder_Q.ckpt.
Every file is checked against the checksum in TrustMark's own source code.
"""
import hashlib
import shutil
import sys
from pathlib import Path

import trustmark
from trustmark.trustmark import MODEL_CHECKSUMS

NEEDED = ["trustmark_Q.yaml", "encoder_Q.ckpt", "decoder_Q.ckpt"]

if len(sys.argv) != 2:
    sys.exit("Usage: uv run python copy_models.py path/to/the/folder/with/the/3/files")

source = Path(sys.argv[1]).expanduser()
target = Path(trustmark.__file__).resolve().parent / "models"
target.mkdir(exist_ok=True)

ok = True
for name in NEEDED:
    file = source / name
    if not file.is_file():
        print(f"{name:18s} MISSING in {source}")
        ok = False
        continue
    checksum = hashlib.md5(file.read_bytes()).hexdigest()
    if checksum != MODEL_CHECKSUMS[name]:
        print(f"{name:18s} WRONG CHECKSUM (the download is damaged, so get it again)")
        ok = False
        continue
    shutil.copyfile(file, target / name)
    print(f"{name:18s} ok, copied")

if not ok:
    sys.exit("Not every file was copied. Fix the lines above, and run this again.")
print(f"All 3 files are in {target}")
