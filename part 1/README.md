# Part 1: Watermarks You Cannot See

In this part, you're going to hide 8 characters inside a photo, prove to yourself that nobody can see them, and then read them back with a detector. After that, you'll edit the photo in order to find out what the watermark can survive (and what it can't).

The watermark comes from TrustMark, which is an open-source watermarking tool from Adobe Research. That's also what the `tm_` at the front of the script names stands for, in case you were wondering.

There are 6 steps, and the entire thing takes about 10 minutes once your laptop is set up.

## Before You Start

You need 2 things:

1. **The setup is done.** If you haven't run `uv sync` yet, go back to the README in the main folder and follow "Set Up Your Laptop" first.
2. **Your terminal is inside the `part 1` folder.** If your terminal is still in the main folder from the setup, run the line below. If you opened a new terminal today, move into the main folder first (the same `cd` line that you used during the setup), and then run it.

```bash
cd "part 1"
```

The quotation marks matter, because the folder name has a space in it.

From here on, you'll type every command in that same terminal, and every command that runs a script starts with `uv run python`. If you're on Windows, every command on this page works in PowerShell exactly as it's written (the only exceptions are the 2 small tables that have their own line for Windows).

You'll also want this folder open in your file manager, because you're going to copy a photo into it and open a few pictures. This line opens it for you:

| System | Command |
|---|---|
| macOS | `open .` |
| Windows | `start .` |
| Linux | `xdg-open .` |

## The Files in This Folder

| File | What it does |
|---|---|
| `tm_encode.py` | Hides 8 characters in a photo (Step 2) |
| `side_by_side.py` | Puts the 2 photos next to each other, and measures the difference (Step 3) |
| `tm_decode.py` | The detector: it tells you whether a picture carries a watermark (Steps 4 and 6) |
| `tm_edits.py` | Edits the watermarked photo 6 ways, and runs the detector on every copy (Step 5) |
| `make_test_image.py` | Optional: makes a test picture when you don't have a photo |
| `copy_models.py` | Only for emergencies: installs the model files by hand (see "If the Model Download Fails") |
| `input/original.jpg` | The photo that everything starts from |
| `output/` | The folder where the scripts write their results |

## Step 1: Choose Your Photo

The `input` folder already has a picture named `original.jpg`, so you can skip straight to Step 2 if you'd like.

However, it's a lot more fun with a photo of your own. First delete the `original.jpg` that's in the `input` folder, and then copy your own JPEG photo into that folder and name it `original.jpg`. A good photo for this has 3 things:

- It's at least 1,024 pixels wide.
- It has texture in it, such as leaves, stone, fabric, or hair. A watermark hides in texture, so a flat logo or a white screenshot is a poor choice.
- It has an ordinary shape. A very wide or very tall picture (more than twice as long on 1 side as on the other) only gets watermarked in its center square.

You don't have to measure anything, because Step 2 prints the size of your photo. Just be sure that the file is a real JPEG (an iPhone photo is often a HEIC file, so export it as a JPEG first), and that its name is exactly `original.jpg`. Windows hides the ending of a file name, so File Explorer shows a correctly named photo as just `original`. If you aren't sure, run `ls input` in your terminal, because it lists the real names (you don't want to see `original.jpg.jpg` there).

## Step 2: Hide 8 Characters in the Photo

Run this in your terminal:

```bash
uv run python tm_encode.py
```

The very first time that you run this, TrustMark downloads its 3 model files (the trained neural network that hides and reads the watermark, about 62 MB in all). So, you'll see 3 lines that start with `Fetching model file (once only)`. Don't worry, because that download really does happen only once, and every later run skips it. (If the terminal sits on a `Fetching` line for more than a few minutes, press Control and C in order to stop it, and jump to "If the Model Download Fails" below.)

Then you'll see 4 lines like these (the time depends on your machine, and the size depends on your photo):

```
photo:    input/original.jpg  (1600 x 1000 pixels)
payload:  'ORLY2026'
encoded in 0.36 seconds
saved:    output/watermarked.png
```

By the way, every script in this part needs about 5 seconds to start, because it has to load PyTorch and the model first. So, a short pause after you press Enter is perfectly normal.

What matters is the last line: there's now a copy of your photo at `output/watermarked.png`, and the text `ORLY2026` is hidden inside its pixels. (The word `payload` is simply the tool's name for the hidden text.)

Now, if you'd like to hide your own text, add the path of the photo and your text to the end of the command. The text can be 8 characters at most, and letters and digits are the safe choice:

```bash
uv run python tm_encode.py input/original.jpg HELLO
```

From then on, your own text shows up wherever the examples below show `ORLY2026`.

## Step 3: Try to Spot the Watermark

Run this in your terminal:

```bash
uv run python side_by_side.py
```

You'll see 5 lines like these. The 3 numbers below come from a test run with the picture that ships in the `input` folder, so your own photo will give you different ones:

```
PSNR:                        46.26 dB
largest single-pixel change: 17 of 255
average pixel change:        0.88 of 255
saved output/side_by_side.png  (the answer is in output/answer.txt)
saved output/difference_x20.png
```

This script made 3 files in the `output` folder, so let's look at them in order.

**First, open `output/side_by_side.png`.** You can double-click it in your file manager (Finder on a Mac, File Explorer on Windows), or you can open it from the terminal:

| System | Command |
|---|---|
| macOS | `open output/side_by_side.png` |
| Windows | `start output\side_by_side.png` |
| Linux | `xdg-open output/side_by_side.png` |

The picture shows your original photo and the watermarked copy next to each other, in a random order. So, which side has the watermark? Go ahead and take a good, long look at both of them, and make your guess before you read on.

**Second, read the answer.** This command prints it, and it works on all 3 systems:

```bash
cat output/answer.txt
```

The answer is a single line, such as `left = original, right = watermarked`. (The script shuffles the 2 photos every time that you run it, so even the person who ran it has to look.)

**Third, open `output/difference_x20.png`** in the same way that you opened the first picture. This is the difference between the 2 photos, made 20 times brighter. The picture is mostly dark, and the faint texture that you can see is the watermark.

Now let's go back to the 3 numbers that the script printed, because each of them tells you how small the change is:

- **PSNR** (peak signal-to-noise ratio) measures how close the 2 photos are, in decibels, so a higher number means a smaller change. TrustMark's own source code says that the model in these scripts typically lands around 43, and the 4 pictures in the test runs for this course landed between about 40 and 46.
- **Largest single-pixel change** is the biggest change that the watermark made to any color value. Every pixel stores its red, green, and blue as numbers from 0 to 255, so that's the scale.
- **Average pixel change** is the typical change, on the same scale.

## Step 4: Run the Detector

First, ask the detector about your original photo:

```bash
uv run python tm_decode.py input/original.jpg
```

You should see this line:

```
input/original.jpg                 no watermark
```

Then ask it about the copy:

```bash
uv run python tm_decode.py output/watermarked.png
```

You should see this line:

```
output/watermarked.png             WATERMARK FOUND   payload='ORLY2026'
```

Did you notice what the detector didn't need in order to give you that answer? It never saw the original photo, and nobody told it what was hidden. It simply read the 8 characters straight out of the pixels, with nothing else to go on.

Now, here's an honest warning, because no detector is perfect. Once in a great while, the detector reads a few characters of nonsense out of a picture that has no watermark at all. In a test with 20,000 patterns of random bits, the check that this detector uses said yes 11 times. So, if the characters that come back aren't the ones that you hid, count that as "no watermark".

## Step 5: Edit the Photo, and Run the Detector Again

Run this in your terminal:

```bash
uv run python tm_edits.py
```

This script makes 6 edited copies of the watermarked photo, and it runs the detector on all of them. It also saves every copy in the `output` folder (as `edit_jpeg_q85.png`, `edit_crop_40pct.png`, and so on), so you can open them and look. Here's what each edit does:

| Edit | What it does to the photo |
|---|---|
| `jpeg_q85` | Saves it as a JPEG at quality 85 (a light squeeze) |
| `jpeg_q50` | Saves it as a JPEG at quality 50 (a heavy squeeze) |
| `resize_50pct` | Shrinks it to 50% of its width and 50% of its height |
| `resize_25pct` | Shrinks it to 25% of its width and 25% of its height |
| `crop_10pct` | Cuts 5% off every side, so 10% of the width and 10% of the height are gone |
| `crop_40pct` | Cuts 20% off every side, so 40% of the width and 40% of the height are gone |

The output has a header, and then you get 1 line per edit. Every line ends with either `FOUND` (plus the 8 characters) or `LOST`. So, this is what a test run printed for the picture that ships in the `input` folder:

```
edit                    size   result
jpeg_q85         1600 x 1000   FOUND   payload='ORLY2026'
jpeg_q50         1600 x 1000   FOUND   payload='ORLY2026'
resize_50pct       800 x 500   FOUND   payload='ORLY2026'
resize_25pct       400 x 250   FOUND   payload='ORLY2026'
crop_10pct        1440 x 900   FOUND   payload='ORLY2026'
crop_40pct         960 x 600   LOST
```

So, go ahead and read down the last column of your own output: every `FOUND` is an edit that your watermark survived (the same 8 characters came back), and every `LOST` is an edit that removed it. Now, your own photo can behave differently, because the results depend on the picture. In the test runs for this course, 3 real photos gave these same 6 results, but a very wide photo also lost its watermark to `jpeg_q50`.

## Step 6: The Screenshot Test

This one doesn't have a script, because you're the one who takes the screenshot. First, here's how to take a screenshot of an area on your system:

| System | How to take a screenshot of an area | Where the file lands |
|---|---|---|
| macOS | Press Shift, Command, and 4 together, and then drag across the photo | On your Desktop |
| Windows | Press the Windows key, Shift, and S together, and then drag across the photo | Click the notification that appears, and save the picture from there |
| Linux | Press the Print Screen key, and choose the option that selects an area | On most desktops, in the Screenshots folder inside Pictures |

Now you have 4 things to do:

1. Open `output/watermarked.png` on your screen, in the same way that you opened the picture in Step 3.
2. Take a screenshot of the photo, and keep your selection just inside the edges of the photo. It's a lot better to cut a little bit off the photo than to capture any of the window around it (you'll see why below).
3. Move the screenshot file into the `output` folder, and rename it `screenshot.png`. Screenshot names are long (and they have spaces in them), so a short name saves you a lot of typing.
4. Run the detector on it:

```bash
uv run python tm_decode.py output/screenshot.png
```

Finally, look at the line that the detector printed. If it says `WATERMARK FOUND`, then your watermark just survived a screenshot! A screenshot is a brand new file, so any label that was attached to the old file is gone, but a watermark is different, because it lives in the pixels themselves.

If it says `no watermark` instead, that's an honest result too, and the most likely reason is the edge of your selection. In the test runs for this course, a capture that cut 10% off every side of the photo still came back `FOUND`. However, a capture that was too big (with a strip of the window around the photo, as thin as 3% of its width) came back with nothing. So, take another screenshot, stay inside the edges this time, and run the test again.

## What You Just Learned

- An invisible watermark is a real signal in the pixels, even though your eyes can't find it.
- The detector gives a clear yes or no, and it doesn't need the original photo.
- A watermark can survive a lot of everyday edits, but not all of them. So, when a detector finds nothing, that doesn't prove that there was never a watermark.

That's it for Part 1! Part 2 moves from pictures to text.

## If the Model Download Fails

In Step 2, TrustMark downloads its model files from `cai-watermark.adobe.net`. Some company networks and VPNs block that site (a test install of this course ran into that block). When that happens, you'll see 2 lines that start with `Error downloading model file`, and the last line reads:

```
TrustMark could not load its model files. See 'If the Model Download Fails' in README.md.
```

The easiest fix is to switch to another network (a phone hotspot works well) and run Step 2 again. If you can't do that, then you can install the 3 files by hand:

1. On any machine that can reach the site, download these 3 files with a browser. If your browser shows a file as text instead of saving it, use the browser's "Save As" command, and keep the exact name.
   - `https://cai-watermark.adobe.net/watermarking/trustmark-models/trustmark_Q.yaml`
   - `https://cai-watermark.adobe.net/watermarking/trustmark-models/encoder_Q.ckpt`
   - `https://cai-watermark.adobe.net/watermarking/trustmark-models/decoder_Q.ckpt`
2. Put all 3 files in the same folder on your laptop (your Downloads folder is fine).
3. From the `part 1` folder, run this command with the path to that folder:

```bash
uv run python copy_models.py ~/Downloads
```

The script checks every file against its checksum in TrustMark's own source code (a checksum is a fingerprint that proves that the file arrived undamaged), and then it copies the files to the right place. You should see 3 lines like these, followed by a line that tells you where the files went:

```
trustmark_Q.yaml   ok, copied
encoder_Q.ckpt     ok, copied
decoder_Q.ckpt     ok, copied
```

After that, go back to Step 2.

## If Something Goes Wrong

| What you see | What it means | What to do |
|---|---|---|
| `can't open file ... No such file or directory` | Your terminal isn't in the `part 1` folder | Move into the main folder, and then run `cd "part 1"` |
| `I can't find input/original.jpg` | The photo in the `input` folder isn't named exactly `original.jpg` | Check for `original.jpeg`, `original.JPG`, or a double ending such as `original.jpg.jpg`. If the photo is gone, run `uv run python make_test_image.py` |
| `isn't a picture that I can open` | The file isn't a real JPEG or PNG (an iPhone HEIC photo, for example) | Export the photo as a JPEG, and copy it in again |
| `I can't find output/watermarked.png` | You skipped Step 2 | Run `uv run python tm_encode.py` first |
| `The payload holds 8 plain ASCII characters at most` | Your text is too long, or it has an accent or an emoji in it | Use 8 characters or fewer, with plain letters and digits |
| `The 2 photos have different sizes` | The photo in `input` changed after Step 2 | Run Step 2 again, and then Step 3 |
| `MISSING` from `copy_models.py` | A file isn't in that folder, or its name changed (for example `trustmark_Q.yaml.txt`) | Fix the name, or point the command at the right folder |
| `WRONG CHECKSUM` from `copy_models.py` | The download was cut off | Download that file again |
| `file not found` from `tm_decode.py` | The path is wrong, or the file's real name isn't what you think it is | Run `ls output` in order to see the real names (on Windows, a renamed file can end up as `screenshot.png.png`), and put the path in quotation marks if it has spaces |
| `WATERMARK FOUND` with characters that you never hid | The detector read nonsense, which is rare but possible | Count it as "no watermark" (see the warning in Step 4) |
