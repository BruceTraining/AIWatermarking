"""DEMO 5 on the slides, Steps 5 and 6 in the README:
write the same text twice, once without a watermark and once with one.

Usage:
    uv run python generate.py                          the story prompt in input/prompt.txt
    uv run python generate.py input/prompt_code.txt    any other prompt file

It reads the prompt, and it writes 3 files:
    output/passage_a.txt and output/passage_b.txt   the 2 texts, in a random order
    output/answer.txt                               which passage carries the watermark

The first run downloads the model (about 724 MB), unless a folder named "model" is here.
"""
import random
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import SynthIDTextWatermarkingConfig

HELP = "See 'If the Model Download Fails' in the README of this folder."
OUT = Path("output")

if not Path("tokenizer").is_dir():
    sys.exit('I can\'t find the tokenizer folder. Run this from the "part 2" folder.')
prompt_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input/prompt.txt")
if not prompt_file.is_file():
    sys.exit(f"I can't find {prompt_file.as_posix()}. Check the file name.")
try:
    PROMPT = prompt_file.read_text(encoding="utf-8-sig").strip()
except UnicodeDecodeError:
    sys.exit(f"{prompt_file.as_posix()} isn't saved as UTF-8 text. "
             "In your editor, use Save As and choose the encoding UTF-8.")
if not PROMPT:
    sys.exit(f"{prompt_file.as_posix()} is empty. Write 1 request in it, and run this again.")

# The model comes from a folder named "model" when there is one, and from Hugging Face when there isn't.
MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct"
if Path("model").is_dir():
    missing = [f for f in ("config.json", "generation_config.json", "model.safetensors")
               if not (Path("model") / f).is_file()]
    if missing:
        sys.exit(f"The model folder is missing {', '.join(missing)}. {HELP}")
    if (Path("model") / "model.safetensors").stat().st_size < 723_000_000:
        sys.exit("model/model.safetensors is incomplete (it should be 723,674,912 bytes). "
                 f"Download it again. {HELP}")
    MODEL = "model"

# The key: 9 numbers. Whoever holds them can detect the watermark, and nobody else can.
keys = [654, 400, 836, 123, 340, 443, 597, 160, 57]
wm = SynthIDTextWatermarkingConfig(keys=keys, ngram_len=5)

print(f"prompt: {PROMPT}")
print(f"loading the model from {MODEL} ...")
tokenizer = AutoTokenizer.from_pretrained("tokenizer")
try:
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32)   # 32-bit floats, no GPU needed
except Exception as error:
    reason = (str(error).strip().splitlines() or [type(error).__name__])[0]
    sys.exit(f"I couldn't load the model. {HELP}\n(The reason given was: {reason})")
model.eval()

chat = [{"role": "user", "content": PROMPT}]
inputs = tokenizer.apply_chat_template(
    chat, add_generation_prompt=True, return_tensors="pt", return_dict=True)
start = inputs["input_ids"].shape[1]

settings = dict(do_sample=True, max_new_tokens=400)

print("writing the text without a watermark ...")
torch.manual_seed(7)                     # the same starting point for both texts
plain  = model.generate(**inputs, **settings)

print("writing the text with a watermark ...")
torch.manual_seed(7)
marked = model.generate(**inputs, **settings,
                        watermarking_config=wm)

texts = [
    ("no watermark", tokenizer.decode(plain[0, start:], skip_special_tokens=True).strip()),
    ("watermarked", tokenizer.decode(marked[0, start:], skip_special_tokens=True).strip()),
]
random.shuffle(texts)
OUT.mkdir(exist_ok=True)
(OUT / "passage_a.txt").write_text(texts[0][1] + "\n", encoding="utf-8")
(OUT / "passage_b.txt").write_text(texts[1][1] + "\n", encoding="utf-8")
(OUT / "answer.txt").write_text(
    f"passage A = {texts[0][0]}, passage B = {texts[1][0]}\n", encoding="utf-8")
print("saved output/passage_a.txt and output/passage_b.txt")
print("(the answer is in output/answer.txt, but ask the detector first)")
