# 🛠️ Class 18 — Building & Deploying Real MCP Servers
**📅 12-13 September 2026** · Agentic AI 3.0 Specialization · Mentor: Mayank Aggarwal

📖 **[Full class summary, diagrams & Q&A →](<../../classes_summary/18 - 12-13 Sep - Building & Deploying MCP Servers.md>)**

---

RecipeBox rebuilt both the official SDK way and the FastMCP way, then extended live with a resource and two prompts; a warm-up server gains real role-scoped authentication; and a full timesheet app (browser UI + MCP server, one shared database) goes from local to a real deployment story.

## 📂 Files in This Folder

| Folder | What it is |
|---|---|
| [`MCP-Precoded/`](<MCP-Precoded/>) | Instructor-provided reference: RecipeBox built twice — raw `mcp` SDK vs. `fastmcp` — same 3 tools, line-count comparison |
| [`first-mcp-server/`](<first-mcp-server/>) | The FastMCP RecipeBox taken further live: + `recipe://tags` resource, + 2 prompts, registered directly with Claude Desktop |
| [`mcp-warmup-primitives/`](<mcp-warmup-primitives/>) | The Class 16/17 warm-up server, now with a resource, a prompt, and (`server_with_auth.py`) real role-scoped auth via static tokens |
| [`TimeTrackProject/timetrack/`](<TimeTrackProject/timetrack/>) | A real timesheet app — FastAPI + FastMCP mounted together, one SQLite database shared by a browser UI and an MCP client |

## ▶️ Run RecipeBox (Either Version)

```bash
cd MCP-Precoded
python3 recipebox_lowlevel.py     # or: python3 recipebox_fastmcp.py
npx @modelcontextprotocol/inspector python3 recipebox_fastmcp.py
```

## ▶️ Run TimeTrack

```bash
cd "TimeTrackProject/timetrack"
uv sync
uv run uvicorn main:app --reload
# website: http://127.0.0.1:8000   ·   MCP endpoint: http://127.0.0.1:8000/mcp
```

## ✅ Action Items

- [ ] Build both RecipeBox versions from `MCP-Precoded/` and count the lines yourself
- [ ] Add one more scoped tool to `mcp-warmup-primitives/server_with_auth.py`, test with each of the three static tokens
- [ ] Run TimeTrack locally, log a time entry from the website, read it back through `get_timesheet` from an MCP client

---
⬆️ [Weekend 11 overview](<../README.md>) · ⬅️ [Class 17](<../../Weekend 10 - 5-6 Sep/06 Sep - MCP Primitives & Architecture/README.md>) · [Course index](<../../README.md>)
