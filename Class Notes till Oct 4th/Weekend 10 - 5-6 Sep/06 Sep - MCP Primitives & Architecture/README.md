# 🔍 Class 17 — MCP Primitives, Architecture Recap & the Wiretap
**📅 6 September 2026** · Agentic AI 3.0 Specialization · Mentor: Mayank Aggarwal

📖 **[Full class summary, diagrams & Q&A →](<../../classes_summary/17 - 6 Sep - MCP Primitives, Architecture & Wiretap.md>)**

---

Finishing what Class 16 deferred: real, running code for all three MCP primitives (tools, resources, prompts) on top of the Class 16 warm-up server, plus a from-scratch wiretap tool that shows the actual JSON-RPC wire protocol live — something Claude Desktop's own logs stopped exposing after a June 2026 update.

## 📂 Files in This Folder

| File | What it is |
|---|---|
| [`v4a_primitives_notebook.ipynb`](<v4a_primitives_notebook.ipynb>) | Tools vs. resources vs. prompts, with real code adding a resource and a prompt to the Class 16 server |
| [`mcp_wiretap.py`](<mcp_wiretap.py>) | Universal MCP wiretap — sits between Claude Desktop and any real server, relaying and pretty-printing every JSON-RPC message |
| [`mcp_wiretap_no_color.py`](<mcp_wiretap_no_color.py>) | Same wiretap, plain output for piping straight to a log file |
| [`claude_desktop_config.example.json`](<claude_desktop_config.example.json>) | Sanitized example config showing the wiretap and a custom server registration pattern (genericized paths — not a real machine's config) |
| [`MCP-Lifecycle.pdf`](<MCP-Lifecycle.pdf>), [`MCP-Primitives.pdf`](<MCP-Primitives.pdf>), [`AI-Updater-Project.pdf`](<AI-Updater-Project.pdf>) | Class handout PDFs |
| [`Link.txt`](<Link.txt>) | A real-world reference server: [`theposch/gmail-mcp`](https://github.com/theposch/gmail-mcp) |

> The architecture notebook from Class 16 (`p2_MCP_Architecture.ipynb`) isn't duplicated here — see [`Weekend 09/23rd Aug - MCP/Complete MCP/`](<../../Weekend 09 - 22-23 Aug/23rd Aug - MCP/Complete MCP/p2_MCP_Architecture.ipynb>) for that file.

## ▶️ Try the Wiretap

```bash
# in claude_desktop_config.json, point a server's "command"/"args" at the wiretap instead:
python3 mcp_wiretap.py -- <the real command and args that used to be there>
```

Restart Claude Desktop fully and use it normally — the terminal (or a `--log` file) shows the complete, real, live JSON-RPC conversation: handshake, capability discovery, every tool call, and shutdown.

## ✅ Action Items

- [ ] Work through `v4a_primitives_notebook.ipynb`: add a resource and a prompt to the Class 16 warm-up server, confirm both show up in Inspector
- [ ] Wiretap a real server you already have configured and read the raw JSON-RPC traffic
- [ ] Genericize any path before copying from `claude_desktop_config.example.json` into your own config

---
⬆️ [Weekend 10 overview](<../README.md>) · ⬅️ [Class 16](<../../Weekend 09 - 22-23 Aug/23rd Aug - MCP/README.md>) · [Course index](<../../README.md>)
