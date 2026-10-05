# 🚀 Live Class 2026 — Agentic AI 3.0 Specialization

**All code, notebooks, diagrams, and class-by-class notes for the live Agentic AI 3.0 Specialization with AgentOps.**
🎙️ Mentor: **Mayank Aggarwal** · 🏫 Krish Naik Academy · 🗓️ Every Saturday & Sunday, 8–11 AM IST

📖 **[Mayank's running notes, Colab links & escalated Q&A →](https://bugs-sleep-6uj.craft.me/agentic3)** · 📄 [Full course brochure (PDF)](<Weekend 01 - 27-28 Jun/02-03 - 28 Jun & 4 Jul - Python Refresher & Pydantic Deep Dive/Agentic-3-0.pdf>)

🧰 **New here? Start with [Prerequisites & First-Time Setup](<PREREQUISITES.md>)** — Python, UV, VS Code, and API keys, all in one place before Class 01.
📖 **Revising a term?** Check the [Glossary](<GLOSSARY.md>) — every recurring concept, one line each, linked back to where it was first taught.
📓 **Want to follow along live?** Every notebook Mayank actually ran in class is indexed in [Live Colab Notebooks](<COLAB_NOTEBOOKS.md>).

---

## 🗺️ How This Repo Is Organized

The course runs **every Saturday & Sunday**, so the repo is organized the same way you attend it: one **`Weekend NN - Date(s)/`** folder per calendar weekend, each nesting the real dated class folder(s) — code, notebooks, and Excalidraw diagrams exactly as built live. Every individual class also gets a **beautifully written summary** in [`classes_summary/`](<classes_summary/>), in the spirit of the mermaid-diagram-driven notes format the course community loves.

```mermaid
flowchart LR
    W["🗓️ Weekend NN folder<br/>joint recap + nav"] --> A["📂 Dated class folder(s) inside it<br/>real code, notebooks, diagrams"]
    A -.pairs with.-> B["📖 classes_summary/NN - Date - Topic.md<br/>recap, diagrams, Q&A, action items"]
    B --> C["🧠 You, actually understanding<br/>what happened in class"]

    style W fill:#f59e0b,color:#fff
    style B fill:#6366f1,color:#fff
    style C fill:#22c55e,color:#fff
```

Open **any** `Weekend NN/` folder on GitHub for a joint recap of both days that weekend, or open a dated class folder inside it and its own `README.md` renders right there with a quick overview and a link to the full write-up — you never have to go hunting for context. A few code folders span two calendar weekends because the same live-coding session continued across them (e.g. Class 02 → Class 03); those live in the earlier weekend, and the later weekend's `README.md` links straight back to it.

---

## 🗓️ Weekend Index

| Weekend | Date(s) | Classes | Folder |
|---|---|---|---|
| 00 | 21 Jun | 00 · Course Induction & Roadmap | [`Weekend 00 - 20-21 Jun/`](<Weekend 00 - 20-21 Jun/>) |
| 01 | 27–28 Jun | 01 · Python Setup & API Basics — 02 · Python Refresher | [`Weekend 01 - 27-28 Jun/`](<Weekend 01 - 27-28 Jun/>) |
| 02 | 4–5 Jul | 03 · Pydantic Deep Dive — 04 · Anatomy of an Agent | [`Weekend 02 - 4-5 Jul/`](<Weekend 02 - 4-5 Jul/>) |
| 03 | 11–12 Jul | 05 · The Agentic Loop — 06 · Introduction to LangChain | [`Weekend 03 - 11-12 Jul/`](<Weekend 03 - 11-12 Jul/>) |
| 04 | 18–19 Jul | 07 · LangChain Family & Harness Engineering — 08 · Inside the Model | [`Weekend 04 - 18-19 Jul/`](<Weekend 04 - 18-19 Jul/>) |
| 05 | 25–26 Jul | 09 · Structured Output Mastery — 10 · Tools Deep Dive | [`Weekend 05 - 25-26 Jul/`](<Weekend 05 - 25-26 Jul/>) |
| 06 | 1 Aug | 11 · Agents, Middleware & Memory | [`Weekend 06 - 1 Aug/`](<Weekend 06 - 1 Aug/>) |
| 07 | 8–9 Aug | 12 · Mastering Middleware — 13 · Guardrails & Tool Resilience | [`Weekend 07 - 8-9 Aug/`](<Weekend 07 - 8-9 Aug/>) |
| 08 | 15–16 Aug | 14 · Shell Tools & Custom Middleware | [`Weekend 08 - 15-16 Aug/`](<Weekend 08 - 15-16 Aug/>) |
| 09 | 22–23 Aug | 15 · Runtime & Human-in-the-Loop — 16 · MCP Begins | [`Weekend 09 - 22-23 Aug/`](<Weekend 09 - 22-23 Aug/>) |
| 10 | 5–6 Sep | 17 · MCP Primitives, Architecture & Wiretap | [`Weekend 10 - 5-6 Sep/`](<Weekend 10 - 5-6 Sep/>) |
| 11 | 12–13 Sep | 18 · Building & Deploying MCP Servers | [`Weekend 11 - 12-13 Sep/`](<Weekend 11 - 12-13 Sep/>) |

> New weekends land as new `Weekend NN - Date(s)/` folders — this table grows with the course.

---

## 📚 Class Index

| # | Date(s) | Class | 📖 Summary | 📂 Code |
|---|---|---|---|---|
| 00 | 21 Jun | Course Induction & Roadmap | [notes](<classes_summary/00 - 21 Jun - Course Induction & Roadmap.md>) | — |
| 01 | 27 Jun | Python Setup & API Basics | [notes](<classes_summary/01 - 27 Jun - Python Setup & API Basics.md>) | [`Weekend 01/01 - 27 Jun .../`](<Weekend 01 - 27-28 Jun/01 - 27 Jun - Python Setup & API Basics/>) |
| 02 | 28 Jun | Python Refresher | [notes](<classes_summary/02 - 28 Jun - Python Refresher.md>) | [`Weekend 01/02-03 - 28 Jun & 4 Jul .../`](<Weekend 01 - 27-28 Jun/02-03 - 28 Jun & 4 Jul - Python Refresher & Pydantic Deep Dive/>) |
| 03 | 4 Jul | Pydantic Deep Dive | [notes](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) | ↑ same folder (in Weekend 01) |
| 04 | 5 Jul | Anatomy of an Agent | [notes](<classes_summary/04 - 5 Jul - Anatomy of an Agent.md>) | [`Weekend 02/04-05 - 5 Jul & 11 Jul .../`](<Weekend 02 - 4-5 Jul/04-05 - 5 Jul & 11 Jul - Anatomy of an Agent & The Agentic Loop/>) |
| 05 | 11 Jul | The Agentic Loop (Pure Python) | [notes](<classes_summary/05 - 11 Jul - The Agentic Loop.md>) | ↑ same folder (in Weekend 02) |
| 06 | 12 Jul | Introduction to LangChain | [notes](<classes_summary/06 - 12 Jul - Introduction to LangChain.md>) | [`Weekend 03/06 - 12 Jul .../`](<Weekend 03 - 11-12 Jul/06 - 12 Jul - Introduction to LangChain/>) |
| 07 | 18 Jul | LangChain Family & Harness Engineering | [notes](<classes_summary/07 - 18 Jul - LangChain Family & Harness Engineering.md>) | [`Weekend 04/07-08 - 18-19 Jul .../`](<Weekend 04 - 18-19 Jul/07-08 - 18-19 Jul - LangChain Family & the Model Layer/>) |
| 08 | 19 Jul | Inside the Model (Params, Streaming, Tools, Structured Output) | [notes](<classes_summary/08 - 19 Jul - Inside the Model.md>) | ↑ same folder |
| 09 | 25 Jul | Structured Output Mastery (CineBot) | [notes](<classes_summary/09 - 25 Jul - Structured Output Mastery.md>) | [`Weekend 05/09-10 - 25-26 Jul .../`](<Weekend 05 - 25-26 Jul/09-10 - 25-26 Jul - Structured Output & Tools (CineBot)/>) |
| 10 | 26 Jul | Tools Deep Dive | [notes](<classes_summary/10 - 26 Jul - Tools Deep Dive.md>) | ↑ same folder |
| 11 | 1 Aug | Agents, Middleware & Memory | [notes](<classes_summary/11 - 01 Aug - Agents, Middleware & Memory.md>) | [`Weekend 06/11-12 - 1-8 Aug .../`](<Weekend 06 - 1 Aug/11-12 - 1-8 Aug - Agents, Memory & Middleware/>) |
| 12 | 8–9 Aug | Mastering Middleware | [notes](<classes_summary/12 - 08 Aug - Mastering Middleware.md>) | ↑ same folder (in Weekend 06) |
| 13 | 9 Aug | Guardrails, Todo Lists & Tool Resilience | [notes](<classes_summary/13 - 09 Aug - Guardrails, Todo Lists & Tool Resilience.md>) | — *(not yet shared)* |
| 14 | 16 Aug | Shell Tools & Custom Middleware | [notes](<classes_summary/14 - 16 Aug - Shell Tools & Custom Middleware.md>) | — *(not yet shared)* |
| 15 | 22 Aug | Runtime Deep Dive & Human-in-the-Loop | [notes](<classes_summary/15 - 22 Aug - Runtime & Human-in-the-Loop.md>) | — *(not yet shared)* |
| 16 | 23 Aug | MCP 1: Why MCP Had to Exist | [notes](<classes_summary/16 - 23 Aug - MCP Introduction.md>) | [`Weekend 09/23rd Aug - MCP/`](<Weekend 09 - 22-23 Aug/23rd Aug - MCP/>) |
| 17 | 6 Sep | MCP Primitives, Architecture Recap & Wiretap | [notes](<classes_summary/17 - 6 Sep - MCP Primitives, Architecture & Wiretap.md>) | [`Weekend 10/06 Sep .../`](<Weekend 10 - 5-6 Sep/06 Sep - MCP Primitives & Architecture/>) |
| 18 | 12–13 Sep | Building & Deploying Real MCP Servers | [notes](<classes_summary/18 - 12-13 Sep - Building & Deploying MCP Servers.md>) | [`Weekend 11/12-13 Sep .../`](<Weekend 11 - 12-13 Sep/12-13 Sep - Building & Deploying MCP Servers/>) |

> New weekends land as new `Weekend NN/` folders + a matching file in `classes_summary/` — this table grows with the course.

---

## 🛣️ The Curriculum Arc

```mermaid
flowchart TD
    P0["🐍 Phase 0 — Foundations<br/>Python, Pydantic, AI vocabulary"] --> P1["🤖 Phase 1 — Agents in Pure Python<br/>Brain → Memory → Tools → Agentic Loop"]
    P1 --> P2["🔗 Phase 2 — LangChain in Depth<br/>Models, Structured Output, Tools, Agents, Middleware"]
    P2 --> P3["🥕 Phase 3 — LangGraph & Beyond<br/>state, checkpointing, MCP, RAG"]
    P3 --> P4["🏗️ Phase 4 — Production Capstones<br/>deployed on Cloud & VPS"]

    style P1 fill:#f59e0b,color:#fff
    style P2 fill:#6366f1,color:#fff
    style P4 fill:#22c55e,color:#fff
```

This repository currently covers **Phase 0 through the end of Phase 2, into Phase 3** (Classes 00–18) — raw-Python fundamentals, all the way through LangChain's full middleware system (built-in and custom), runtime internals, human-in-the-loop, and the MCP module from first principles through real, deployed servers.

## 🎬 Recurring Projects You'll See Throughout

| Project | First appears | What it is |
|---|---|---|
| **Project Zero** | Class 04 | The hand-built raw-Python agent — model, tools, memory, Streamlit UI |
| **CineBot** | Class 09 | A movie-ticket booking agent — the vehicle for Structured Output & Tools |
| **TripMate** | Class 11 | A travel-planning agent with real weather, search, and SQLite persistence |

## 🧰 Tooling Used Across the Course

- 🐍 **Python 3.10+** managed with **[UV](https://docs.astral.sh/uv/)** — every class folder with code has its own `pyproject.toml`
- 🔑 Free-tier LLM access via **Groq** and **OpenRouter**; paid via **OpenAI** / **Anthropic** — always via `.env`, never committed (`.env.example` ships in every project instead)
- 📓 **Google Colab** for line-by-line learning; **VS Code** for real, multi-file projects
- 🎨 **Excalidraw** for the architecture diagrams sketched live in class

## 🔗 More Resources

- 📖 [Mayank's Craft notes](https://bugs-sleep-6uj.craft.me/agentic3) — links for every class, Colab notebooks, doubt-solving MayankGPT
- 🛡️ [Mastering Pydantic](https://pydantic-with-mayank.netlify.app) · 🧠 [AI Terms](https://ai-terms-with-mayank.netlify.app) · 🐍 [Agents with Pure Python](https://python-agents-with-mayank.netlify.app/) · 💾 [AI Memory Lab](https://context-with-mayank.netlify.app/)
- 🔌 [MCP Lifecycle — Conversation Simulator](https://mcp-lifecycle-simulator.netlify.app) · [MCP Lifecycle — Complete Guide](https://mcp-lifecycle.netlify.app)
- 🔍 [Transformer Explainer](https://poloclub.github.io/transformer-explainer/)

## ▶️ Running Any Class's Code

Every code folder is an independent [UV](https://docs.astral.sh/uv/) project — `cd` into the dated class folder *inside* its `Weekend NN/` parent:

```bash
cd "Weekend 03 - 11-12 Jul/06 - 12 Jul - Introduction to LangChain"
uv sync
cp .env.example .env   # fill in at least one free key
uv run main.py
```

---

*Questions about a specific class? Open its folder's `README.md` on GitHub for the quick overview, or the matching file in [`classes_summary/`](<classes_summary/>) for the full write-up with diagrams and Q&A.*
