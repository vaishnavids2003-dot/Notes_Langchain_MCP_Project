# 📖 Glossary — Agentic AI 3.0

Every term below was taught live, with real code — this page just collects them in one alphabetical list with a link back to where each was first built, so revision doesn't mean re-reading twelve classes end to end.

> 🔎 Looking for the deep explanation, not just the definition? Click through to the linked class summary — each one builds the term from real code, not just describes it.

---

| Term | One-line definition | First taught |
|---|---|---|
| **Agent** | Model + tools + memory + a loop that decides what to do next — not just a chat reply | [Class 04](<classes_summary/04 - 5 Jul - Anatomy of an Agent.md>) |
| **Agentic Loop** | The cycle of: model reasons → picks a tool → tool runs → result goes back to the model → repeat until done | [Class 05](<classes_summary/05 - 11 Jul - The Agentic Loop.md>) |
| **`args_schema`** | A Pydantic model attached to a tool for constraints richer than plain type hints (ranges, regex, nested fields) | [Class 10](<classes_summary/10 - 26 Jul - Tools Deep Dive.md>) |
| **`BaseModel`** | Pydantic's base class — define a shape once, get parsing + validation for free | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |
| **Context Window** | The model's fixed-size "whiteboard" — oldest content is silently erased once it fills up | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |
| **`create_agent()`** | LangChain's single entry point for assembling a model, tools, system prompt, and middleware into a runnable agent | [Class 06](<classes_summary/06 - 12 Jul - Introduction to LangChain.md>) |
| **Deep Agents** | The "batteries-included" tier of the LangChain family — zero control, maximum defaults | [Class 07](<classes_summary/07 - 18 Jul - LangChain Family & Harness Engineering.md>) |
| **`field_validator`** | A Pydantic decorator for custom validation rules on a single field, beyond what `Field()` constraints express | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |
| **Guardrail vs. Middleware** | A guardrail blocks/filters based on a fixed rule; middleware is the general mechanism guardrails (and much else — retries, fallback, logging) are built from | [Class 12](<classes_summary/12 - 08 Aug - Mastering Middleware.md>) |
| **Harness** | Everything wrapped around a raw model call — prompt, tools, memory — that turns a model into an agent | [Class 06](<classes_summary/06 - 12 Jul - Introduction to LangChain.md>) |
| **Hooks (`before_agent`, `before_model`, `wrap_model_call`, `after_model`, `wrap_tool_call`, `after_agent`)** | The six points custom middleware can intercept agent execution at — `before_agent`/`after_agent` run once per run, the rest can run multiple times per agentic loop | [Class 14](<classes_summary/14 - 16 Aug - Shell Tools & Custom Middleware.md>) |
| **Host / Client / Server (MCP)** | The host is the app a person uses (Claude Desktop, VS Code); it starts a dedicated MCP client for each server, and the client is the one that actually talks to the server | [Class 16](<classes_summary/16 - 23 Aug - MCP Introduction.md>) |
| **Human-in-the-Loop (HITL)** | Middleware that pauses execution for real human approval before a sensitive action (e.g. a refund) proceeds — four decisions: `approve`, `edit`, `reject`, `respond` | [Class 11](<classes_summary/11 - 01 Aug - Agents, Middleware & Memory.md>) · [Class 15](<classes_summary/15 - 22 Aug - Runtime & Human-in-the-Loop.md>) |
| **JSON-RPC 2.0** | The message format MCP clients and servers actually speak over — not plain REST | [Class 16](<classes_summary/16 - 23 Aug - MCP Introduction.md>) |
| **LangChain** | The mid-control tier of the family — "a real kitchen, you control the spice level" | [Class 06](<classes_summary/06 - 12 Jul - Introduction to LangChain.md>) · [Class 07](<classes_summary/07 - 18 Jul - LangChain Family & Harness Engineering.md>) |
| **LangGraph** | The low-level, total-control tier LangChain is built on top of — state, checkpointing, durable execution | [Class 07](<classes_summary/07 - 18 Jul - LangChain Family & Harness Engineering.md>) |
| **LangSmith** | The observability layer — a full trace of every model call, tool call, and middleware decision, with latency and token cost per step | [Class 07](<classes_summary/07 - 18 Jul - LangChain Family & Harness Engineering.md>) |
| **LLM** | Predicts the next *token*, not the next word — pattern completion, not understanding | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |
| **`LLMToolSelectorMiddleware`** | Uses a (possibly cheaper) model to filter which tools are relevant to the *current query* before the main model call — a different axis from state-based dynamic tool loading | [Class 13](<classes_summary/13 - 09 Aug - Guardrails, Todo Lists & Tool Resilience.md>) |
| **Luhn Algorithm** | The checksum real credit card numbers satisfy — why `PIIMiddleware`'s credit-card detector won't flag an arbitrary digit string that fails it | [Class 13](<classes_summary/13 - 09 Aug - Guardrails, Todo Lists & Tool Resilience.md>) |
| **MCP (Model Context Protocol)** | An open protocol — not another wrapper — so an application exposes its tools/resources/prompts once and any AI host can connect to it the same way | [Class 16](<classes_summary/16 - 23 Aug - MCP Introduction.md>) |
| **MCP Primitives (Tools, Resources, Prompts)** | The three things an MCP server can offer a client: Tools (something that *does*), Resources (something to *read*), Prompts (a *form* to fill in) | [Class 16](<classes_summary/16 - 23 Aug - MCP Introduction.md>) |
| **Middleware** | A hook that sits between the agent and the model/tools to observe or modify what happens — limits, fallback, PII redaction, retry, and more | [Class 11](<classes_summary/11 - 01 Aug - Agents, Middleware & Memory.md>) · [Class 12](<classes_summary/12 - 08 Aug - Mastering Middleware.md>) |
| **`model.profile`** | Checks whether a given model actually supports structured output *before* you rely on it, instead of finding out at runtime | [Class 09](<classes_summary/09 - 25 Jul - Structured Output Mastery.md>) |
| **Nested Models** | A Pydantic `BaseModel` field whose type is itself another `BaseModel` — validated recursively | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |
| **Parameters** | Billions of fixed weights set at training time — not the same thing as tokens | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |
| **PIIMiddleware** | Built-in middleware that detects and masks/redacts personally identifiable information in tool inputs or outputs — mapped directly to real HIPAA requirements | [Class 12](<classes_summary/12 - 08 Aug - Mastering Middleware.md>) |
| **`ProviderStrategy` vs. `ToolStrategy`** | Two ways to get structured output: the provider's own native feature (fast, only where supported) vs. a synthetic tool call that fakes it (works almost anywhere) | [Class 08](<classes_summary/08 - 19 Jul - Inside the Model.md>) |
| **ReAct** | The 2022 paper behind the first general-purpose agents — the model generates JSON that gets hand-parsed into a tool call | [Class 07](<classes_summary/07 - 18 Jul - LangChain Family & Harness Engineering.md>) |
| **`return_direct`** | A tool flag that skips the model's rephrasing pass and returns the tool's raw output straight to the user | [Class 10](<classes_summary/10 - 26 Jul - Tools Deep Dive.md>) |
| **Runtime** | Information that isn't part of the conversation but still travels with the agent everywhere — five components: `context`, `store`, `stream_writer`, `execution_info`, `server_info` | [Class 15](<classes_summary/15 - 22 Aug - Runtime & Human-in-the-Loop.md>) |
| **`ShellToolMiddleware`** | Gives an agent a real, persistent shell — the entire mechanism behind how Claude Code, Cursor, and GitHub Copilot actually create and edit files on a machine | [Class 14](<classes_summary/14 - 16 Aug - Shell Tools & Custom Middleware.md>) |
| **Stateless (LLM calls)** | Every model call starts with zero memory of any previous call — any "memory" an agent has is something you built and passed back in yourself | [Class 04](<classes_summary/04 - 5 Jul - Anatomy of an Agent.md>) |
| **Streaming (`AIMessageChunk`)** | Model output arrives in incremental chunks that sum together with `+` into the final full message | [Class 08](<classes_summary/08 - 19 Jul - Inside the Model.md>) |
| **Structured Output** | Forcing a model's reply into a guaranteed, validated shape (a Pydantic schema) instead of trusting free-form text | [Class 04](<classes_summary/04 - 5 Jul - Anatomy of an Agent.md>) · [Class 09](<classes_summary/09 - 25 Jul - Structured Output Mastery.md>) |
| **`TodoListMiddleware`** | Gives an agent a structured, persisted planning object it actually maintains turn over turn — plain system-prompt instructions alone don't reliably produce this | [Class 13](<classes_summary/13 - 09 Aug - Guardrails, Todo Lists & Tool Resilience.md>) |
| **Tokens** | The billing currency — roughly ¾ of a word each; output tokens cost more than input tokens | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |
| **Tool** | A function the model can choose to call itself, given only its name/description/schema — not something you call and paste the result back in for it | [Class 01](<classes_summary/01 - 27 Jun - Python Setup & API Basics.md>) · [Class 06](<classes_summary/06 - 12 Jul - Introduction to LangChain.md>) |
| **`ToolCallLimitMiddleware`** | Caps how often a tool can fire — `run_limit` per single `.invoke()`, `thread_limit` across the whole conversation (needs a checkpointer) | [Class 12](<classes_summary/12 - 08 Aug - Mastering Middleware.md>) · [Class 13](<classes_summary/13 - 09 Aug - Guardrails, Todo Lists & Tool Resilience.md>) |
| **`ToolRuntime`** | The mechanism giving a tool access to run-scoped context (memory, store, config) at call time — "the mirror" a tool checks itself in | [Class 10](<classes_summary/10 - 26 Jul - Tools Deep Dive.md>) |
| **Union (multi-intent)** | Typing a structured-output field as `Union[...]` so a single schema can capture more than one possible intent in a real user message | [Class 09](<classes_summary/09 - 25 Jul - Structured Output Mastery.md>) |
| **Vector Embeddings** | Words become coordinates — similar meaning lands close together in that space | [Class 03](<classes_summary/03 - 4 Jul - Pydantic Deep Dive.md>) |

---

⬆️ [Course index](<README.md>) · 🧰 [Prerequisites & First-Time Setup](<PREREQUISITES.md>)
