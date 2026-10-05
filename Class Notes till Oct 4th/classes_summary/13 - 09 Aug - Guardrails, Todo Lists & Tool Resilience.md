# 🛡️ Class 13 — Guardrails, Todo Lists, Tool Selection & Resilient Tools
### Agentic AI 3.0 Specialization | Live Class 2026

**🎙️ Mentor:** Mayank Aggarwal · **📅 Date:** 9 August 2026 · **⏱️ Duration:** ~4.5 hours

> 📂 **Code for this class:** *(not yet shared in this repo — notes compiled from the live session; `cinebot_tools` continues from Class 11–12)*

---

Finishes **Tool Call Limit** carried over from Class 12, then works through the remaining built-in middlewares: guardrails, PII (in depth), To-Do List, LLM Tool Selector, Tool Error, Tool Retry, and LLM Tool Emulator.

## 🔢 Finishing Tool Call Limit: Run vs. Thread

**Run limit** caps calls within a single `.invoke()`; **thread limit** caps the total across an entire conversation, tracked via the checkpointer. Mayank's analogy: a run limit of 4 caps chapatis in one sitting, a thread limit of 10 caps the whole day however it's split across meals.

## 🛡️ Guardrails: The Highway Analogy

> *"A guardrail is a way to control the AI agent's behavior — that's it, nothing else."*

A barrier on a mountain road keeps a car from going over the edge; a barrier on a highway keeps it from swerving into oncoming traffic — the same idea bounds what an agent can say or do. **Guardrail vs. middleware, restated:** a guardrail is the *goal* (protecting the agent from doing something undesirable); middleware is one *mechanism* for achieving it, alongside system-prompt instructions or third-party libraries. Even a simple tool call limit already counts as a guardrail. "Compliance" itself isn't defined by the framework — it's defined externally (HIPAA, GDPR, SOC 2).

## 🕵️ PII Detection, Revisited in Depth

```python
from langchain.agents.middleware import PIIMiddleware

pii_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
)
```

A live debugging moment: a test credit card wasn't caught on the first attempt — LangChain's credit-card detector validates using the **Luhn algorithm**, the real checksum card numbers satisfy, so an arbitrary digit string that fails it simply won't register.

**Strategies, with the fourth option added:**

| Strategy | Behavior |
|---|---|
| `block` | Raises an exception the moment PII is detected — halts the flow |
| `redact` | Replaces PII with a placeholder type label — original value fully gone |
| `mask` | Partially obscures the value (e.g. last few digits only) |
| `hash` | Deterministic hash — same input always maps to the same hash, preserving identity without exposing the real value |

For a company-specific ID format, custom detection is necessary:

```python
import re
from langchain.agents.middleware import PIIMiddleware

def detect_booking_code(content: str) -> list[dict]:
    """Detect CineBot's own booking code format: BK followed by 4 digits."""
    matches = []
    for match in re.finditer(r"BK\d{4}", content):
        matches.append({"text": match.group(0), "start": match.start(), "end": match.end()})
    return matches

custom_pii_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[PIIMiddleware("booking_code", detector=detect_booking_code, strategy="hash")],
)
```

On real payment details: the better pattern than ever letting card numbers pass through the AI is a **headless tool** — a secure payment page the user interacts with directly, entirely outside the model's view.

## ✅ Todo List Middleware

```python
from langchain.agents.middleware import TodoListMiddleware

todo_agent = create_agent(model="openai:gpt-5-mini", tools=cinebot_tools, middleware=[TodoListMiddleware()])
result = todo_agent.invoke({"messages": [("user",
    "I want to plan a movie night: check what's showing, pick something good, and book 2 seats.")]})
```

Plain system-prompt instructions don't reliably produce a *maintained*, structured object the model keeps updating turn over turn — this middleware is what gives an agent that structured planning object, the same scaffolding behind tools like Claude Code feeling more capable at multi-step tasks. Requires a checkpointer, since the list must persist and update across turns.

## 🎯 LLM Tool Selector — Choosing Tools by Query, Not by State

Dynamic tool loading (earlier class) filters by known **state** (VIP or not). This filters by **what's being asked** — if an agent has 15 tools, does every query need all 15 sent to the model?

```python
from langchain.agents.middleware import LLMToolSelectorMiddleware, wrap_model_call

selector_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[
        LLMToolSelectorMiddleware(model="openai:gpt-5-mini", max_tools=2, always_include=["check_showtimes"]),
    ],
)

@wrap_model_call
def show_tools(request, handler):
    print("\nTOOLS SENT TO MODEL:", [tool.name for tool in request.tools])
    return handler(request)
```

`always_include` tools are always kept and don't count against `max_tools`. Live queries confirmed real filtering: a refund question sent only `check_showtimes` + `get_refund_policy`; a cancellation sent `cancel_booking` and related tools — never the full six. If you already *know* a tool should never be available to a given user, that decision belongs in your own code, not an LLM's judgment — reserve the selector for genuinely query-dependent relevance.

## ⚠️ Tool Error Middleware — Failing Gracefully, Without Retrying

```python
from langchain.agents.middleware import ToolErrorMiddleware

def on_seat_error(exc: Exception, request) -> str | None:
    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed with {type(exc).__name__}. Please provide a valid seat number like 'A12'."
    return None  # anything else propagates and halts the run

error_handled_agent = create_agent(
    model="openai:gpt-5-mini", tools=cinebot_tools, middleware=[ToolErrorMiddleware(on_error=on_seat_error)],
)
```

Without this, an unhandled tool exception halts the entire agent run — still just Python underneath. `on_error` takes a single function; returning a string becomes the tool message sent back to the model, `None` lets the original exception propagate. Return the **exception type**, not the raw message, so internals never leak. This middleware does **not** auto-retry — that's the next one.

## 🔁 Tool Retry Middleware — Automatic Exponential Backoff

```python
from langchain.agents.middleware import ToolRetryMiddleware

resilient_tool_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[flaky_showtime_check],
    middleware=[ToolRetryMiddleware(max_retries=3, backoff_factor=2.0, initial_delay=1.0, on_failure="continue")],
)
```

`max_retries` counts retries **after** the initial call (`max_retries=3` → up to 4 total calls). Defaults: `max_retries=2, backoff_factor=2.0, initial_delay=1.0, max_delay=60.0, jitter=True, on_failure="continue"`. Backoff: `delay = initial_delay × (backoff_factor ^ retry_number)` — 1s, 2s, 4s. `jitter` adds randomness so clients don't retry in lockstep.

**A surprising live result:** the flaky-tool demo produced **8 total calls, not 4** — after the first 4 failed, `on_failure="continue"` returned the failure as a tool message, and the model *itself* independently asked to try again, triggering a second full cycle. `ToolRetryMiddleware` only controls its own retry count — it can't stop the model from separately deciding to retry after seeing a failure message.

## 🧪 LLM Tool Emulator — Faking Tool Calls for Testing

```python
from langchain.agents.middleware import LLMToolEmulator

emulated_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[LLMToolEmulator(tools=["book_seats", "cancel_booking"], model="openai:gpt-5-mini")],
)
```

Lets a model *simulate* a plausible tool response without ever executing the real tool — deliberately for testing/development, validating an agent's logic without the cost, risk, or side effects of a real action. Not passing `tools=` emulates every tool by default.

## 💬 Live Q&A Highlights

| Question | Answer |
|---|---|
| Tool Error vs. Tool Retry middleware? | Error handles a failure gracefully once, no retry. Retry actively retries the call itself, with backoff. |
| Do `always_include` tools count against `max_tools`? | No — always sent, don't count against the limit. |
| Can `on_error` support more than one handler? | No — a single function, with full access to the exception, tool name, and request. |
| Why 8 calls instead of 4 with `max_retries=3`? | The middleware's own cycle is 4; the model itself asked for another attempt after seeing the failure — its own fuzzy, non-deterministic behavior, not a bug. |

## ✅ Action Items

- [ ] 🔢 Recreate the tool call limit demo with both a global `run_limit` and a tool-specific `thread_limit`
- [ ] 🕵️ Build a custom PII detector for an ID format relevant to your own use case, and try all four strategies
- [ ] ✅ Add `TodoListMiddleware` to a multi-tool agent with a genuinely multi-step request
- [ ] 🎯 Build the `show_tools` custom middleware yourself and verify `LLMToolSelectorMiddleware`'s filtering
- [ ] ⚠️ Write a tool that raises `ValueError`, wrap it with `ToolErrorMiddleware`, confirm no crash
- [ ] 🔁 Set up `ToolRetryMiddleware` on an always-failing tool and verify the backoff timing
- [ ] 🧪 Try `LLMToolEmulator` on a tool you don't want to call for real yet

---
*Part of the [Live-Class-2026](../README.md) class summary index · ⬆️ [Weekend 07 overview](<../Weekend 07 - 8-9 Aug/README.md>). ⬅️ [Class 12](<12 - 08 Aug - Mastering Middleware.md>) · ➡️ [Class 14](<14 - 16 Aug - Shell Tools & Custom Middleware.md>)*
