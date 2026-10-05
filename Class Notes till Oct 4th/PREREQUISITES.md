# 🧰 Prerequisites & First-Time Setup

**One-time setup for the whole course — do this once, before Class 01, and every `Weekend NN/` project folder from then on works the same way.**

If you're joining mid-course, this page is also your fastest way to catch up on the environment side without re-reading every class's write-up.

---

## 1. Install Python 3.10+ (course projects pin 3.13)

Check what you have:

```bash
python3 --version
```

If it's below 3.10, install a current Python from [python.org](https://www.python.org/downloads/) or your OS package manager. Individual project folders pin an exact version via `.python-version` — UV (next step) reads that automatically, so you don't need to juggle versions by hand.

## 2. Install UV — the package & project manager used all course long

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # Mac / Linux
```

Windows: use Git Bash or Windows Terminal (never plain CMD/PowerShell — see [Class 01](<classes_summary/01 - 27 Jun - Python Setup & API Basics.md>)) and follow the [UV install docs](https://docs.astral.sh/uv/getting-started/installation/).

**Why UV, not pip + venv + conda?** One fast tool replaces the juggling act. Every class folder with code ships its own `pyproject.toml` and `uv.lock` — the exact Python version and dependency list any machine can reproduce identically, the same role `package.json` plays in Node.

## 3. Install VS Code

This is an *Agentic AI* course, not classic Data Science — the workflow leans on `.py` scripts, a real terminal (you'll SSH into cloud machines later in the course), and proper debugging, not just notebooks. Get it from [code.visualstudio.com](https://code.visualstudio.com/).

## 4. Get at least one free LLM API key

Every class folder needs *at least one* provider key to run its live calls. Two are free:

| Provider | Cost | Get a key |
|---|---|---|
| **Groq** | Free, fast | [console.groq.com/keys](https://console.groq.com/keys) |
| **OpenRouter** | Free tier (`model="openrouter/free"` auto-routes so it never goes stale) | [openrouter.ai/keys](https://openrouter.ai/keys) |
| OpenAI | Paid | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| Anthropic | Paid | [console.anthropic.com](https://console.anthropic.com/) |

You only need **one** to get started — Groq is the fastest to sign up for.

## 5. The `.env` workflow — every project folder, same pattern

Every folder with code ships a `.env.example` template. Never edit that file directly — copy it:

```bash
cd "Weekend 01 - 27-28 Jun/01 - 27 Jun - Python Setup & API Basics"
uv sync
cp .env.example .env
# open .env and paste in at least one real key, e.g.:
#   GROQ_API_KEY=gsk_your_real_key_here
uv run main.py
```

`.env` is git-ignored at the repo root — a real key will never get committed by accident. `.env.example` is the only one that ever ships with placeholder values.

## 6. If `git clone` or `git pull` fails

This repo is checked on every push so it should clone cleanly on Windows, macOS and Linux. If it doesn't:

| Symptom | Fix |
|---|---|
| `error: invalid path '...'` or `unable to checkout working tree` | A bad filename slipped in. Tell Mayank the exact path from the error — it's a one-line fix on his side. Then run `git restore --source=HEAD :/` (after the fix is pushed, `git pull`). |
| `Filename too long` (Windows) | Run `git config --global core.longpaths true`, and clone somewhere short like `C:\src\` instead of a deep OneDrive/Documents folder. |
| `Your local changes would be overwritten by merge` on `git pull` | Save your work first with `git stash -u`, run `git pull`, then `git stash pop`. |
| A folder you created never shows up on GitHub | It probably has its own hidden `.git` folder (`uv init` creates one). Delete `<folder>/.git`, or create projects with `uv init --no-vcs`. |

## ✅ Before Class 01

- [ ] Python 3.10+ and UV installed, `uv --version` runs
- [ ] VS Code installed
- [ ] At least one free API key (Groq or OpenRouter) in hand
- [ ] Bookmarked [Mayank's Craft notes](https://bugs-sleep-6uj.craft.me/agentic3) — used for the entire course
- [ ] Blocked Saturday & Sunday, 8–11 AM IST on your calendar

---

⬆️ [Course index](<README.md>) · ➡️ [Weekend 00 — Induction](<Weekend 00 - 20-21 Jun/README.md>)
