# Part 2: Adding and Detecting Text Watermarks

In this part, you're going to read 2 short stories that came from the very same model and the very same prompt, and you're going to guess which one carries a hidden watermark. Then a detector settles it for you with a single command. After that, you'll write 2 stories of your own (1 with a watermark and 1 without), and you'll find out what the detector needs in order to do its job.

So, here's what's under the hood of the scripts that you're about to run. The watermark comes from SynthID-Text, which is the method that Google DeepMind published in 2024. It's built into Transformers, the open-source library from Hugging Face that these scripts use (Hugging Face is also the website that hosts open models). The model that writes the stories is SmolLM2-360M-Instruct, a small open model that's sized for a laptop, so you don't need an account or a graphics card.

Now, there are 6 steps in all. The first 4 are quick, because the repository ships everything that they need. Step 5 downloads the model first (about 724 MB), and Step 6 uses it again, so you'll wait a little longer for those.

## Before You Start

You need 2 things:

1. **The setup is done.** If you haven't run `uv sync` yet, go back to the README in the main folder and follow "Set Up Your Laptop" first. If you already did the setup for Part 1, then you're done, because that same command installed everything for Part 2 as well.
2. **Your terminal is inside the `part 2` folder.** If your terminal is still in the `part 1` folder, run `cd ..` first in order to get back to the main folder. If you opened a new terminal today, move into the main folder first (the same `cd` line that you used during the setup). Then run this line:

```bash
cd "part 2"
```

Be sure to keep the quotation marks, because the folder name has a space in it.

From here on, you'll type every command in that same terminal, and every command that runs a script starts with `uv run python`. If you're on Windows, use PowerShell (and not the older Command Prompt), because every command on this page should work there as it stands.

## The Files in This Folder

| File | What it does |
|---|---|
| `detect.py` | The detector: it tells you whether a text carries the watermark (Steps 2 through 6) |
| `generate.py` | The writer: it asks the model for the same text twice, once without a watermark and once with one (Steps 5 and 6) |
| `input/passage_a.txt` and `input/passage_b.txt` | The 2 stories from the course slides, ready for the detector |
| `input/prompt.txt` | The prompt that both stories came from |
| `input/prompt_code.txt` | A second prompt that asks for code instead of a story (Step 6) |
| `tokenizer/` | The model's tokenizer, which splits a text into tokens. Both scripts need it, so please leave this folder alone |
| `output/` | The folder where `generate.py` writes its results |

Now, you're going to see the word "token" a lot on this page, so here's what it means. A language model doesn't write letters or whole words. It writes tokens, and a token is simply a small piece of text (a short word, or a piece of a longer word). Each of our stories is 400 tokens long, which works out to about 330 words.

## Step 1: Read the 2 Passages, and Make Your Guess

Both stories came from this prompt: "Write a short story about a lighthouse keeper who finds a message in a bottle." The model wrote 400 tokens each time, so both stories stop in the middle of a sentence (that's normal, and it doesn't matter here).

Print the first story in your terminal:

```bash
cat input/passage_a.txt
```

Then print the second one:

```bash
cat input/passage_b.txt
```

If you'd rather read them in a window, you can also open the 2 files in any text editor.

So, here's the question: which passage carries the watermark, A or B? Go ahead and read them as carefully as you like, and make your guess before you move on. (Don't judge the stories too harshly, by the way. This is a very small model, and its lighthouse keepers do some strange things.)

## Step 2: Run the Detector

Now that you've made your guess, let's ask the detector. A watermark is placed with a secret list of numbers called the key, and the detector needs that same key in order to find it (our detector already has it). Run this in your terminal:

```bash
uv run python detect.py input/passage_a.txt input/passage_b.txt
```

After a few seconds (the script has to load its libraries first, and the very first run takes the longest), you should see these 3 lines, with these numbers:

```
text                     tokens   heads  z-score   result
input/passage_a.txt         394   64.6%    17.33   WATERMARK DETECTED
input/passage_b.txt         392   48.7%    -1.52   not detected
```

So, the answer is Passage A. If that wasn't your guess, don't worry, because nobody can read a text watermark off the page (and that's the point).


## What's Actually Happening Here

Now let's go through the columns, because each one tells you a part of the story:

- **tokens** is the number of tokens that the detector counted. It skips the first 4 tokens of a text, and it skips a token when the 4 tokens in front of it are an exact repeat of something earlier in the text. That's why you see 394 and 392 here, and not 400.
- **heads** is where the watermark shows up. The key is a list of 9 numbers, and with it the detector can redo 9 hidden coin flips for every token. Text that was written without the key lands on heads about 50% of the time, like any fair coin. However, when the model wrote Passage A, the watermark kept nudging it toward the words that land on heads. So, Passage A scored 64.6% heads across 3,546 coin flips, and that's a lot more than luck can explain.
- **z-score** turns that percentage into a single number: it tells you how far the text landed from 50%, measured in units of "how far luck alone usually takes you". Ordinary text scores somewhere near 0, and most of the time it stays between -2 and 2.
- **result** says `WATERMARK DETECTED` when the z-score is 4 or more (that number is called the threshold). With fair coins, you'd expect a score that high about once in 30,000 tries.

Did you notice what the detector didn't need? Well, it never loaded the model, and it never saw the prompt, so all it had to work with was the text and the key.

Here's an honest note about that threshold of 4, because no detector is perfect. In a test for this course, the detector's scoring code went through 11,049 pieces of ordinary text (737 documentation and license files from a Linux machine, cut into pieces of 400 tokens, and then again into pieces of 200). The highest z-score was 3.48, so not a single one reached 4. That's a good sign, but you should treat it as a test and not as a guarantee.

## Step 3: Watch the Score Grow

Now, let's find out how much text the detector needs. In order to do that, run the detector again with the `--by-length` option, which makes it read only the first 25 tokens of each passage, then the first 50, and so on:

```bash
uv run python detect.py --by-length input/passage_a.txt input/passage_b.txt
```

You should see this:

```
tokens read      input/passage_a.txt      input/passage_b.txt
         25               z =   3.27               z =  -1.53
         50               z =   5.01               z =  -1.28
        100               z =   7.55               z =  -1.09
        200               z =  11.38               z =  -1.81
        400               z =  17.33               z =  -1.52
```

As you can see, Passage B wanders between -1 and -2, far under the threshold, no matter how much of it the detector reads. Passage A is a different story: after 25 tokens its score is 3.27, which is still under the threshold of 4, and after 400 tokens it's 17.33. Every token adds 9 more coin flips, so the evidence keeps piling up.

This is the reason that a detector can't tell you much about a single sentence. Our story was already over the threshold after 50 tokens, but other kinds of text need a lot more than that (you'll see why in Step 6).

## Step 4: Try the Wrong Key

So far, the detector has used the same key that placed the watermark. Now let's see what happens when it doesn't have that key, which is what the `--wrong-key` option is for (it swaps in 9 other numbers):

```bash
uv run python detect.py --wrong-key input/passage_a.txt input/passage_b.txt
```

You should see this:

```
using a wrong key: [1, 2, 3, 4, 5, 6, 7, 8, 9]
text                     tokens   heads  z-score   result
input/passage_a.txt         394   49.3%    -0.81   not detected
input/passage_b.txt         392   50.9%     1.11   not detected
```

Passage A still carries its watermark, of course, because the text didn't change. However, a detector with the wrong key can't see it, so now both passages look like ordinary text.

Remember this result, because it's the situation that you and I are in with Claude, ChatGPT, and Gemini. This detector only knows our key, and no company has published its own, which means that it can't tell you anything about their text (and "not detected" never means that a human wrote it).

By the way, the real key is the line that starts with `keys = [654` in both scripts. It's the example key that ships with the Transformers library, so it's fine for a course and a terrible idea for a real product, where the key has to stay secret.

## Step 5: Write 2 Stories of Your Own

Now it's your turn to place a watermark. Run this in your terminal:

```bash
uv run python generate.py
```

Here's what you'll see, 1 line at a time (a progress bar that says `Loading weights` shows up among these lines too):

```
prompt: Write a short story about a lighthouse keeper who finds a message in a bottle.
loading the model from HuggingFaceTB/SmolLM2-360M-Instruct ...
writing the text without a watermark ...
writing the text with a watermark ...
saved output/passage_a.txt and output/passage_b.txt
(the answer is in output/answer.txt, but ask the detector first)
```

Now, the very first time that you run this, the script pauses after the `loading the model` line, because that's when it downloads the model from Hugging Face (about 724 MB). You'll probably see progress bars while it does, and the good news is that the download should happen only once.

You may see a few warnings during that download, too. If a line mentions `HF_TOKEN` or an unauthenticated request, you can ignore it, because this model doesn't need an account. On Windows, there may also be a long warning about symlinks and Developer Mode, and you can ignore that one too. (If the download fails, jump to "If the Model Download Fails" below.)

Now, be patient with the 2 `writing` lines, because the model runs on your laptop's processor. On the test machine for this course (which has only 2 processor cores), each story took about 40 seconds. And if you ever need to stop a script, press Control and C together.

The script put your 2 stories in a random order, so you don't know which one is which. Read them first if you'd like (`cat output/passage_a.txt` and `cat output/passage_b.txt`), and then ask the detector:

```bash
uv run python detect.py output/passage_a.txt output/passage_b.txt
```

Finally, check the detector's answer against the truth:

```bash
cat output/answer.txt
```

The answer is a single line, such as `passage A = no watermark, passage B = watermarked`. If the detector said `WATERMARK DETECTED` for the passage that this line calls watermarked, then congratulations, because you just watermarked a text and detected it yourself!

Now, 2 things may surprise you here. First, your stories may be the same 2 stories that ship in the `input` folder, or they may be different ones. The script always starts from the same fixed random seed (that's the starting number for the model's random choices). However, different processors round their numbers a little differently, and a tiny difference is enough to send a story down another path.

Second, if you run the script again, you get the same 2 stories again (possibly in the other order). In order to get a brand new pair, open `generate.py` in a text editor and change the 7 in both `torch.manual_seed(7)` lines to any other number.

Before you move on, take a look at how the watermark got there, too. If you open `generate.py` and find the 2 lines that call `model.generate`, you'll see that they're identical, except that the second one has 1 more setting at the end: `watermarking_config=wm`. That's all it takes.

Here are 2 small notes before you start the last step. On Windows, a story may show odd characters such as `â€™` in your terminal. If that happens, only the display is wrong (the file is fine), so open the file in Notepad instead.

Also, the model that you downloaded should be in Hugging Face's cache (a folder named `.cache/huggingface` in your home folder, outside of this project). You can delete that folder once you're done with the course.

## Step 6: Ask for Code Instead of a Story

Now, a story gives the model a lot of freedom, because there are many good ways to say that the sea was stormy. So, let's find out what happens when the model has less freedom. The file `input/prompt_code.txt` holds a different prompt: "Write a Python function that checks whether a number is prime, and then show 3 examples of calling it." Hand that file to the script:

```bash
uv run python generate.py input/prompt_code.txt
```

Be careful here: this run replaces the 2 stories and the answer from Step 5 in the `output` folder. So, if you'd like to keep your stories, copy them somewhere else first.

Then ask the detector, and check the truth, just like before:

```bash
uv run python detect.py output/passage_a.txt output/passage_b.txt
```

```bash
cat output/answer.txt
```

Your numbers will depend on your run, so here's what a test run for this course gave. The watermarked answer was short (about 200 tokens, of which the detector counted 157), and its z-score was only 1.52. So, the detector said `not detected` for both answers, even though 1 of them really was watermarked! (If your own watermarked answer does get detected, that's not a bug either, because a longer answer carries more signal.)

Why did that happen? Well, code has to be exact: after `def is_prime(n` there's really only 1 good next token, so the watermark has nothing to choose between, and it leaves almost no signal behind. Facts seem to do the same thing to a smaller degree, as you can see from these 3 scores. In the same test run, the story scored 17.33 (with 394 tokens counted), a list of facts about the planets scored 12.06 (393 counted), and a shorter list of capital cities scored 9.26 (286 counted). Treat that gap as a hint and not as a measurement, though, because the 9 test stories (this one included) scored anywhere from 12.3 to 17.3.

If you'd like to try a prompt of your own, save your request in a new text file in the `input` folder (name it `my_prompt.txt`, for example), and then run `uv run python generate.py input/my_prompt.txt`. Please don't trust this little model's code or its facts, though. In that test run, it placed Jupiter right after Mercury.

## What You Just Learned

- A text watermark hides in the model's word choices, so there's nothing for you to see on the page, and no hidden characters are added.
- The detector needs the text and the key. It doesn't need the model, and without the right key it finds nothing.
- The z-score grows with the length of the text, and it shrinks when the model has fewer words to choose from (as it does with code and facts).
- So, a high z-score is strong evidence that a text carries this watermark. A low one proves nothing at all: the text may be too short, it may be code, it may come from a model with another key, or a person may have written it.

That's it for Part 2, and for the course! A watermark is evidence, and it's never proof.

## If the Model Download Fails

Remember that in Step 5, the script downloads the model from `huggingface.co`. However, some company networks and VPNs block that site (the test machine for this course couldn't reach it either). When that happens to you, the script stops with these 2 lines, possibly after a few lines about retries:

```
I couldn't load the model. See 'If the Model Download Fails' in the README of this folder.
(The reason given was: ...)
```

The easiest fix is to switch to another network (a phone hotspot works well) and run Step 5 again. If you can't do that, then you can install the model by hand:

1. Create a new folder named `model` inside the `part 2` folder (right next to `generate.py`). From your terminal, `mkdir model` does it on every system.
2. On any machine that can reach the site, download these 3 files with a browser. If your browser shows a file as text instead of saving it, use the browser's "Save As" command, and keep the exact name.
   - [config.json](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct/resolve/main/config.json)
   - [generation_config.json](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct/resolve/main/generation_config.json)
   - [model.safetensors](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct/resolve/main/model.safetensors)
3. Copy all 3 files into the `model` folder on your laptop. The last one is the big one (723,674,912 bytes, which your system may show as 724 MB or as 690 MB), so be sure that it finished downloading before you copy it.

After that, run Step 5 again. This time, the second line that the script prints should read `loading the model from model ...`, which tells you that it found your folder.

## If Something Goes Wrong

| What you see | What it means | What to do |
|---|---|---|
| `cd: no such file or directory: part 2` (or "Cannot find path" on Windows) | Your terminal isn't in the main folder | Move into the main folder first (the folder that holds `pyproject.toml`), and then run `cd "part 2"` |
| `cat: input/passage_a.txt: No such file or directory`, or `can't open file ... No such file or directory` | Your terminal isn't in the `part 2` folder | Move into the main folder, and then run `cd "part 2"` |
| `'cat' is not recognized` on Windows | You're in the Command Prompt, and not in PowerShell | Close that window, open PowerShell, and move into the `part 2` folder again |
| `No module named 'torch'`, `command not found: python`, or "Python was not found" | The command doesn't start with `uv run` | Type the command again, and start it with `uv run python` |
| `I can't find the tokenizer folder` | Your terminal isn't in the `part 2` folder, or the `tokenizer` folder was moved | Run `cd "part 2"` from the main folder. If the folder is gone, download the code again |
| `I can't find input/passage_a.txt` (or another file name) | The path has a typo, or the file isn't there | Run `ls input` or `ls output` in order to see the real names |
| `I can't find output/passage_a.txt` | You haven't run Step 5 yet | Run `uv run python generate.py` first |
| `I couldn't load the model` | The download from Hugging Face failed, or a file in your `model` folder is damaged | See "If the Model Download Fails" above |
| `The model folder is missing ...` | Your `model` folder doesn't have all 3 files, or a name changed (for example `config.json.txt`) | Fix the names, or download the missing file again |
| `model/model.safetensors is incomplete` | The big download was cut off | Download that file again, and wait until it finishes |
| `isn't saved as UTF-8 text` | You gave a script a Word document, a PDF, or a text file in an older encoding | Copy the text into a plain text file (one that ends in `.txt`). In your editor, choose "Save As" and pick the encoding UTF-8 |
| `I don't know the option` | An option has a typo | The 2 options are `--by-length` and `--wrong-key`, each with 2 hyphens in front |
| `(too short)` in the `--by-length` table | The text has fewer tokens than that row asks for | Nothing is wrong. Read the rows that do have a score |
| `too short to check` in the result column | The text has fewer than 5 tokens | Give the detector a longer text |
| The script seems to hang on a `writing` line | The model is working. It wrote about 10 tokens per second on the 2-core test machine | Give it a few minutes |
| `Killed`, `zsh: killed`, or a message about memory during Step 5 or Step 6 | Your laptop ran out of memory (the model needs about 3 GB) | Close a few programs, and run the step again |
| The detector says `not detected` for a passage that `answer.txt` calls watermarked | The text is short, or it's code or a list of facts (see Step 6) | That's a real result and not a bug. Try a prompt that asks for a longer story |

Last but certainly not least, the files in the `tokenizer` folder come from SmolLM2-360M-Instruct by Hugging Face, which is released under the Apache 2.0 license.
