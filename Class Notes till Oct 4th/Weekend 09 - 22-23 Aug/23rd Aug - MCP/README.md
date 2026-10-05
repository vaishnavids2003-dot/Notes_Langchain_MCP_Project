# 🔌 Class 16 — MCP 1: Why MCP Had to Exist
**📅 23 August 2026** · Agentic AI 3.0 Specialization · Mentor: Mayank Aggarwal

📖 **[Full class summary, diagrams & Q&A →](<../../classes_summary/16 - 23 Aug - MCP Introduction.md>)**

---

Day 1 of the MCP module: why MCP had to exist (function calling → the scaling problem → a shared protocol), the host/client/server architecture, JSON-RPC transport, the three MCP primitives (tools, resources, prompts), and a live end-to-end local server built with [FastMCP](https://gofastmcp.com/).

## 📂 Files in This Folder

| File | What it is |
|---|---|
| [`Complete MCP/p2_MCP_Architecture.ipynb`](<Complete MCP/p2_MCP_Architecture.ipynb>) | The full architecture walkthrough notebook |
| [`Complete MCP/Why MCP Had to Exist.txt`](<Complete MCP/Why MCP Had to Exist.txt>) | The motivating story, in plain text |
| [`Complete MCP/Commands.txt`](<Complete MCP/Commands.txt>) | Every terminal command used in the live demo |
| [`Complete MCP/Complete-MCP.pdf`](<Complete MCP/Complete-MCP.pdf>) | Exported PDF version of the session's material |
| [`Complete MCP/mcp-warmup/`](<Complete MCP/mcp-warmup/>) | The warm-up FastMCP server itself — `server.py` with `greet` and `add` tools |

## ▶️ Run the Warm-Up Server

```bash
cd "Complete MCP/mcp-warmup"
uv sync
uv run fastmcp dev server.py   # opens MCP Inspector at http://127.0.0.1:6274
```

## ✅ Action Items

- [ ] Work through `p2_MCP_Architecture.ipynb` end-to-end: build `server.py`, run it, call `greet`/`add` from Inspector
- [ ] Try the `Ctrl+C` safety test — kill the running server while Inspector is connected, confirm only that one connection closes
- [ ] Register the same server as a STDIO server in VS Code and/or a custom connector in Claude Desktop

---
⬆️ [Weekend 09 overview](<../README.md>) · ⬅️ [Class 15](<../../classes_summary/15 - 22 Aug - Runtime & Human-in-the-Loop.md>) · [Course index](<../../README.md>)
