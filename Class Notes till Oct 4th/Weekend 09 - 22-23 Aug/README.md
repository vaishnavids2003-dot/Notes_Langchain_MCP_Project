# 🗓️ Weekend 09 — 22-23 Aug — Runtime, HITL & MCP Begins

**Agentic AI 3.0 Specialization · Live Class 2026 · Mentor: Mayank Aggarwal**

Saturday closes out the LangChain-native middleware arc with runtime internals and human-in-the-loop; Sunday opens an entirely new module — MCP, taught deliberately independent of any framework first.

```mermaid
flowchart LR
    A["🧠 Class 15, Sat 22 Aug<br/>Runtime & Human-in-the-Loop"] --> B["🔌 Class 16, Sun 23 Aug<br/>MCP Begins"]
    style A fill:#6366f1,color:#fff
    style B fill:#22c55e,color:#fff
```

## 📖 This Weekend's Classes

| Class | Topic | Full write-up | Code |
|---|---|---|---|
| 15 | Runtime Deep Dive & Human-in-the-Loop in Depth | [classes_summary →](<../classes_summary/15 - 22 Aug - Runtime & Human-in-the-Loop.md>) | [`22nd Aug - Runtime & HITL/`](<22nd Aug - Runtime & HITL/>) |
| 16 | MCP 1: Why MCP Had to Exist | [classes_summary →](<../classes_summary/16 - 23 Aug - MCP Introduction.md>) | [`23rd Aug - MCP/`](<23rd Aug - MCP/>) |

Class 15 finally pins down runtime's five components (context, store, stream_writer, execution_info, server_info) against state and tool_runtime, then goes deep on `HumanInTheLoopMiddleware` — the four decision types (`approve`, `edit`, `reject`, `respond`) and conditional interrupts based on a tool call's actual arguments. Class 16 opens the MCP module: why it had to exist (function calling's scaling problem → a shared protocol), the host/client/server architecture, and a real local FastMCP server built and connected live.

🔗 Live Colab used in class: [Class 15 — Runtime & HITL](https://colab.research.google.com/drive/1dFuLlELzyS2NDIBgeVOowrqGJGFPERSL?usp=sharing)

## 🔁 Weekend Navigation

⬅️ [Weekend 08 — 15-16 Aug](<../Weekend 08 - 15-16 Aug/README.md>) · ⬆️ [Course index](<../README.md>) · ➡️ [Weekend 10 — 5-6 Sep](<../Weekend 10 - 5-6 Sep/README.md>)
