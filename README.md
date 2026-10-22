# AI Text Watermarking and Detection

Welcome! This repository holds the code for the O'Reilly live course "AI Text Watermarking and Detection" by Bruce Hopkins. The course is 1 hour long and it comes in 2 parts, so you'll find the code organized in the same way (1 folder per part).

You don't have to run anything during the course, because every result is on the slides. However, I really hope that you run it all yourself afterward, and this page gets your laptop ready for that.

## What Is in Each Folder

| Folder | Part | What you'll find there |
|---|---|---|
| `part 1/` | Part 1: Watermarks You Cannot See | The scripts that hide a watermark in a photo, detect it, and test it against everyday edits |
| `part 2/` | Part 2: Adding and Detecting Text Watermarks | The script that writes the same story twice (with and without a watermark), the detector that tells the 2 versions apart, and 2 sample stories |

Each part folder has an `input/` folder (what the part starts from) and an `output/` folder (where the scripts write their results). Each part also has its own README with the steps, 1 command at a time.

## What You Need to Know First

- You're comfortable reading and running Python scripts from the command line
- You have a basic idea of how a language model picks its next word (tokens, temperature, and sampling), and you don't need any math beyond averages and standard deviations
- You've used Claude, ChatGPT, or Gemini before (as a user)

Now, if the first 2 don't describe you yet, don't worry. You can still do every step in both parts, because each one is a line that you copy and paste. You don't need an account anywhere, and nothing here costs money.

## What Your Laptop Needs

Before you install anything, check your laptop against these 3 things:

- It's a Mac with Apple silicon (an M1 chip or newer) that runs macOS 14 or newer, a Windows PC with a 64-bit Intel or AMD processor, or a Linux machine.
- It has enough free disk space, which is about 7 GB on Linux. However, macOS and Windows should need less than that, because they skip a set of large GPU libraries. (The language model of Part 2 adds about 724 MB on every system, and it lands in a cache folder in your home folder.)
- It has about 3 GB of memory to spare. The last 2 steps of Part 2 need that much, because they run a small language model on your laptop.

The reason for that first bullet is PyTorch (the machine-learning library that the models in both parts run on). The version that this course is tested with isn't published for Intel Macs, for older versions of macOS, or for Windows on ARM. So, if that's your laptop, you can still follow along, because every result is on the slides.

## Set Up Your Laptop (You Only Do This Once)

The setup is 4 steps, and it works the same way on macOS, Windows, and Linux, except that Step 1 has a different line for Windows. Most of the time goes to a single download in Step 3, so that's a good moment to go get a coffee.

### Step 1: Install uv

uv is a tool that installs Python and Python packages for you (it's fast, and it never touches the Python that's already on your machine). If you already have uv, skip to Step 2.

First, you need a terminal window. If you rarely use one, here's how to open it:

| System | How to open a terminal |
|---|---|
| macOS | Press Command and the space bar together, type `Terminal`, and press Return |
| Windows | Click the Start button, type `PowerShell`, and press Enter |
| Linux | Look for "Terminal" in your applications |

From here on, whenever this page says "run" or "paste", it means that you paste the line into that window and then press Enter.

On macOS or Linux, paste this line:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows, paste this line:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Now close that window and open a new one (this part is easy to forget, and uv won't be found until you do it). Then check that uv is there:

```bash
uv --version
```

You should see a version line that starts like `uv 0.11.32`. Your number will probably be newer, and that's fine.

### Step 2: Get the Code

There are 2 ways to get the code, and you only need 1 of them.

**If you use git,** paste these 2 lines into your new terminal window, 1 at a time:

```bash
git clone https://github.com/BruceTraining/AIWatermarking.git
cd AIWatermarking
```

The first line downloads the code into a new folder named `AIWatermarking`, and the second line moves your terminal into that folder.

**If you don't use git,** that's no problem at all:

1. Scroll to the top of the repository page in your browser, click the green "Code" button, and choose "Download ZIP".
2. Unzip the file. On a Mac, double-click it. On Windows, right-click the file, choose "Extract All", and click "Extract". You now have a folder named `AIWatermarking-main`.
3. Move your terminal into that folder. Type `cd` and a space, drag the folder from your file manager into the terminal window (that types the path for you), and press Enter. If you'd rather type the path yourself, and the folder is in Downloads, the line is `cd "Downloads/AIWatermarking-main"`.
4. On Windows, "Extract All" often puts the folder inside another folder with the same name. So, if Step 3 below complains that it can't find `pyproject.toml`, run `cd AIWatermarking-main` and try again.

Either way, your terminal is now inside the main folder of the code, which is the folder that holds this README and a file named `pyproject.toml`. The rest of this page calls it "the main folder".

### Step 3: Install Everything with 1 Command

This step takes a few minutes, because PyTorch is a big download, and the terminal can sit quietly for a while. So, be sure that your terminal is in the main folder, and then run this:

```bash
uv sync
```

That single command does 3 things for you:

1. It downloads Python 3.12 if you don't have it yet (and it leaves any other Python on your machine alone).
2. It creates a folder named `.venv` inside the main folder.
3. It installs the exact package versions that are recorded in the `uv.lock` file, so you get the same versions that these scripts were tested with.

On Linux, a test install of this course took up about 5.5 GB of disk space, and most of that is NVIDIA's GPU libraries. Those libraries aren't installed on macOS and Windows, so the download is smaller there.

### Step 4: Check That It Worked

Now run this line in order to check that everything landed. The first run can take a little while before anything appears, so give it a moment:

```bash
uv run python -c "import trustmark, transformers, torch; print('ready, torch', torch.__version__)"
```

You should see a line that starts like this:

```
ready, torch 2.14.1
```

Don't worry if you see a suffix after the version number, because that's normal. On Linux, for example, it reads `2.14.1+cu130`.

Did you notice the `uv run` at the front of that command? Every command that runs a script in this course starts with it, because it puts the command inside the project's own environment, which is the `.venv` folder from Step 3. So, you never have to activate anything by hand.

## Where to Go Next

Your laptop is ready! Now open the README of Part 1, which is the file named `README.md` inside the `part 1` folder (on GitHub, click the `part 1` folder at the top of the repository page). Its "Before You Start" section moves your terminal into that folder. When you're done there, the `part 2` folder has a README of its own, and it picks up where Part 1 stops.

## If Something Goes Wrong

| What you see | What it means | What to do |
|---|---|---|
| `command not found: uv` or `uv: command not found` (or "uv is not recognized" on Windows) | Your terminal was already open when uv was installed | Close the terminal, open a new one, and try again |
| `curl: command not found` on Linux | Your machine doesn't have curl | Paste this line instead: `wget -qO- https://astral.sh/uv/install.sh \| sh` |
| `command not found: git` or `git: command not found` (or "git is not recognized" on Windows) | You don't have git | Use the "Download ZIP" route in Step 2. On a Mac, a window may offer to install the developer tools instead, and you can accept that too |
| `cd` says that it can't find the folder | The folder isn't where the line says it is, or the ZIP file isn't unzipped yet | Unzip the file, and then drag the folder into the terminal after `cd` and a space |
| ``error: No `pyproject.toml` found in current directory or any parent directory`` | Your terminal isn't inside the main folder | Use `cd` to move into the folder that holds this README. After a ZIP download on Windows, the right folder can be 1 level deeper |
| `uv sync` stops with an error that mentions `torch` and your platform | PyTorch 2.14.1 isn't published for your machine (see "What Your Laptop Needs") | Use another machine, or follow along with the slides |
| `uv sync` stops with a network error | The download was interrupted, or your network blocks it | Run `uv sync` again, because uv keeps the files that it already downloaded. If it keeps failing, switch to another network (a phone hotspot works well) |
| `No space left on device` (or "There is not enough space on the disk" on Windows) | The disk is full | Free up about 7 GB, and then run `uv sync` again |
