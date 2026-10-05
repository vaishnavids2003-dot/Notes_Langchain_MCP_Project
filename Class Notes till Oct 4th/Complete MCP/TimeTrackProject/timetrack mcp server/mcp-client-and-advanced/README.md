# Building Your Own MCP Client — Complete, Numbered, Self-Contained

Everything in this folder is a *complete* file — nothing here needs you
to copy-paste a snippet into another file to make it work. `main.py`
already has every tool in it. Every file in `client/` runs on its own.

## Folder layout

```
client_project/
├── database.py      <- persistence, shared by every tool
├── main.py           <- the COMPLETE TimeTrack server, all tools included
└── client/
    ├── 01_raw_client.py                <- the verbose, three-layer way
    ├── 02_fastmcp_client.py            <- the easy, one-object way
    ├── 03_agent_loop.py                <- a real agent, no framework
    ├── 04_sampling_demo.py             <- server borrows the client's LLM
    ├── 05_elicitation_demo.py          <- server asks a real question mid-task
    ├── 06_ping_and_errors.py           <- a real ping, a real error
    ├── 07_timeout_and_cancellation.py  <- a real timeout, triggering cancellation
    └── 08_progress_notifications.py    <- real progress updates, watched live
```

## Setup

```bash
pip install mcp fastmcp anthropic
export ANTHROPIC_API_KEY=your-key-here   # needed for 03, 04
```

## Run order

Run every numbered file **from inside the `client/` folder**, in order —
each one builds on the idea from the one before it:

```bash
cd client
python3 01_raw_client.py                # heads up: may hang on macOS, see below
python3 02_fastmcp_client.py
python3 03_agent_loop.py
python3 04_sampling_demo.py
python3 05_elicitation_demo.py
python3 06_ping_and_errors.py
python3 07_timeout_and_cancellation.py
python3 08_progress_notifications.py
```

You never need to run `main.py` by itself first — each client script
launches it automatically as a subprocess.

## A real, currently open bug — file 01 specifically

`01_raw_client.py` uses the official SDK's low-level `stdio_client()`,
which has a documented, currently open bug: it **hangs forever on
macOS**. If it hangs, that's the known issue, not your code — move on to
`02_fastmcp_client.py`, which does the same thing safely and is what
every file after it uses.

## An honest note on sampling (file 04)

`ctx.sample()` — used inside `summarize_week` in `main.py` — now
triggers an SDK deprecation warning in your terminal. It still works, on
the protocol version FastMCP speaks today. It's a real, current
transition in the ecosystem (toward calling an LLM provider directly
instead), not something broken.

## What's genuinely tested here

Every piece of tool logic in `main.py` — `summarize_week`,
`log_time_with_confirmation` (all three outcomes: normal hours, high
hours confirmed, high hours declined), and `slow_tool`'s progress
reporting — was tested directly with mock objects standing in for
`ctx.sample()` / `ctx.elicit()` / `ctx.report_progress()` before this was
written. The agent loop's control flow (`03_agent_loop.py`) was
separately tested the same way, confirmed to call exactly one tool and
terminate correctly. `database.py` was tested against a real, on-disk
SQLite file, including a genuine restart-and-recover check.
