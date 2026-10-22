"""DEMO 6 on the slides, Steps 2 through 6 in the README:
ask the detector whether a text carries the watermark.

Usage:
    uv run python detect.py input/passage_a.txt input/passage_b.txt
    uv run python detect.py --by-length input/passage_a.txt input/passage_b.txt
    uv run python detect.py --wrong-key input/passage_a.txt input/passage_b.txt

The detector needs the text and the key, and nothing else. It never loads the model.
"""
import math
import sys
from pathlib import Path

import torch
from transformers import AutoTokenizer, SynthIDTextWatermarkLogitsProcessor

# The key: the same 9 numbers that generate.py used. A detector with other numbers finds nothing.
keys = [654, 400, 836, 123, 340, 443, 597, 160, 57]
THRESHOLD = 4.0          # a z-score of 4 or more is very hard to explain with luck

EXAMPLE = "    uv run python detect.py input/passage_a.txt input/passage_b.txt"
OPTIONS = ("--by-length", "--wrong-key")
args = sys.argv[1:]
unknown = [a for a in args if a.startswith("-") and a not in OPTIONS]
if unknown:
    sys.exit(f"I don't know the option {unknown[0]}. The 2 options are --by-length and --wrong-key "
             "(each with 2 hyphens in front).")
by_length = "--by-length" in args
if "--wrong-key" in args:
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9]   # 9 other numbers, in order to show what a wrong key finds
    print("using a wrong key:", keys)
paths = [Path(a) for a in args if a not in OPTIONS]
if not paths:
    sys.exit("Give me at least 1 text file, for example:\n" + EXAMPLE)
if not Path("tokenizer").is_dir():
    sys.exit('I can\'t find the tokenizer folder. Run this from the "part 2" folder.')

# Only the tokenizer is needed (it splits the text into the pieces that the model wrote).
tokenizer = AutoTokenizer.from_pretrained("tokenizer")
tokenizer.model_max_length = 10**9      # the detector reads a text of any length
flipper = SynthIDTextWatermarkLogitsProcessor(
    keys=keys, ngram_len=5, sampling_table_size=65536, sampling_table_seed=0,
    context_history_size=1024, device=torch.device("cpu"))


def score(token_ids):
    """Redo the 9 coin flips for every token. Return (tokens counted, share of heads, z-score)."""
    if len(token_ids) < 5:
        return 0, 0.5, 0.0
    ids = torch.tensor([token_ids], dtype=torch.long)
    flips = flipper.compute_g_values(ids).float()                    # 1 = heads, 0 = tails
    counted = flipper.compute_context_repetition_mask(ids).float()   # skip repeated phrases
    n = int(counted.sum().item())
    if n == 0:
        return 0, 0.5, 0.0
    total = flips.shape[-1] * n                                      # 9 flips per token
    heads = (flips * counted[..., None]).sum().item() / total
    z = (heads - 0.5) * 2.0 * math.sqrt(total)                       # a fair coin gives about 0
    return n, heads, z


def verdict(n, z):
    if n == 0:
        return "too short to check"
    return "WATERMARK DETECTED" if z >= THRESHOLD else "not detected"


texts = []
for path in paths:
    if not path.is_file():
        sys.exit(f"I can't find {path.as_posix()}. Check the file name.")
    try:
        text = path.read_text(encoding="utf-8-sig").strip()
    except UnicodeDecodeError:
        sys.exit(f"{path.as_posix()} isn't saved as UTF-8 text. Save it as a plain text file (.txt) "
                 "with the encoding UTF-8, and try again.")
    texts.append((path.as_posix(), tokenizer(text, add_special_tokens=False).input_ids))

if by_length:
    print(f"{'tokens read':>11s}   " + "   ".join(f"{name:>22s}" for name, _ in texts))
    for length in (25, 50, 100, 200, 400):
        row = [f"z = {score(ids[:length])[2]:6.2f}" if len(ids) >= length else "(too short)"
               for _, ids in texts]
        print(f"{length:11d}   " + "   ".join(f"{cell:>22s}" for cell in row))
else:
    print(f"{'text':24s} {'tokens':>6s} {'heads':>7s} {'z-score':>8s}   result")
    for name, ids in texts:
        n, heads, z = score(ids)
        print(f"{name:24s} {n:6d} {heads:7.1%} {z:8.2f}   {verdict(n, z)}")
