# LangChain Practical — `langchain-course`

Real `uv`-based LangChain project for **[Class 07](<../../../../classes_summary/07 - 18 Jul - LangChain Family & Harness Engineering.md>)** (18 July 2026): environment setup, `init_chat_model`, and message types, hands-on in VS Code rather than a notebook.

## Structure

| Path | Covers |
|---|---|
| `Learning/Part - 0 Overview/` | FAQs collected during setup |
| `Learning/Part 1 - Environment Setup/` | `commands.txt`, `setup_check.ipynb` |
| `Learning/Part 2 - Models/` | `init_chat_model`, provider swapping |
| `Learning/Part 3 - Messages/` | `messages.py` — System/Human/AI message types |

## Setup

```bash
uv sync
cp .env.example .env   # add at least one provider key
uv run main.py
```

---
⬅️ Back to [Class 07-08 overview](<../../README.md>)
