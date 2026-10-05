# 🧵 Class 12 — Mastering Middleware: Limits, Fallback, PII, Retry & Tool Emulation
### Agentic AI 3.0 Specialization | Live Class 2026

**🎙️ Mentor:** Mayank Aggarwal · **📅 Date:** 8–9 August 2026 · **⏱️ Duration:** ~4.5 hours (the notebook's own cells mark a real "9th August" continuation mid-session)

> 📂 **Code for this class:** [`11-12 - 1-8 Aug - Agents, Memory & Middleware/MIddleware.ipynb`](<../Weekend 06 - 1 Aug/11-12 - 1-8 Aug - Agents, Memory & Middleware/MIddleware.ipynb>) (cells 57–end) · [`Agent-Middleware-Architecture.excalidraw`](<../Weekend 06 - 1 Aug/11-12 - 1-8 Aug - Agents, Memory & Middleware/Agent-Middleware-Architecture.excalidraw>)
> 🔗 Live Colab used in class: [Middleware notebook](https://colab.research.google.com/drive/1Qt9uU2HhDvtFTWwbbFBYxK86jJypv1w_?usp=sharing)

---

This session runs through **nine** built-in middlewares end to end — considerably more than the six usually cited — each demonstrated against the same `cinebot_tools` from Class 11.

## 🔢 Model Call Limit — Run vs. Thread, the Real Analogy

The whiteboard draws this distinction with a genuinely memorable analogy, captioned directly on the drawing: **"Breakfast, Lunch, Dinner"** next to **"run limit — Chappatis allowed per meal"** and **"thread limit — Chappatis allowed total across all meals."** A run limit caps one sitting; a thread limit caps the whole day, no matter how many sittings.

```python
call_limited_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    checkpointer=InMemorySaver(),  # required for thread_limit to persist across calls
    middleware=[
        ModelCallLimitMiddleware(   # low values taken just for example
            thread_limit=5,          # across the WHOLE conversation
            run_limit=2,             # per single .invoke() call
            exit_behavior="end",     # graceful stop, not an exception
        ),
    ],
)
```

## 🔀 Model Fallback

```python
resilient_agent = create_agent(
    model="openai:gpt-5.5-haiku",     # primary, most capable
    tools=cinebot_tools,
    middleware=[
        ModelFallbackMiddleware(
            "openai:gpt-5-mini",   # fallback -- cheaper, still OpenAI, needs no extra setup
            # "ollama:llama3.2",   # a further, fully-local last resort
        ),
    ],
)
```

The whiteboard's version of this same idea is drawn as a blunt, honest failure message: **"AI -> I am unable to connect."** — the exact user-facing symptom `ModelFallbackMiddleware` exists to prevent.

## 🛠️ Tool Call Limit — Per-Tool, Not Just Global

```python
tool_limited_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    checkpointer=InMemorySaver(),
    middleware=[
        ToolCallLimitMiddleware(run_limit=8),                                          # global, this turn
        ToolCallLimitMiddleware(tool_name="cancel_booking", thread_limit=2, run_limit=1),  # tighter, ONE tool
    ],
)
```

The whiteboard's real worked numbers for this: **8** (global run limit) next to **1** and **2** — captioned *"2 (Thread or Conversation Limit)"* — with a booking-ID trail literally sketched as `B100, B101, B102` to show three attempted cancellations against a `thread_limit=2` cap.

## 🕵️ PII Detection — Including a Custom Detector for CineBot's Own Data

```python
pii_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
)
```

Real test input from class: *"My email is priya@example.com and my credit card is 4111-1111-1111-1234, can you check showtimes for Dune Part Two?"* — the email is stripped entirely before the model ever sees it; the card number is masked, not removed, so the model can still tell *something* sensitive was present.

Since booking codes are CineBot's own domain-specific format, no built-in detector covers them — so the class wrote one, using a plain regex:

```python
import re

def detect_booking_code(content: str) -> list[dict]:
    """Detect CineBot's own booking code format: BK followed by 4 digits."""
    matches = []
    for match in re.finditer(r"BK\d{4}", content):
        matches.append({"text": match.group(0), "start": match.start(), "end": match.end()})
    return matches

custom_pii_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[PIIMiddleware("booking_code", detector=detect_booking_code, strategy="mask")],
)
```

The real Excalidraw board lists the actual regulated-ID categories discussed alongside the generic **Email / Mobile Number** pair: **Aadhaar** and **PAN** — India-specific government ID formats, called out by name as exactly the kind of country-specific identifier no framework ships a built-in detector for, and exactly why the custom-detector pattern above matters in practice.

## ✅ To-Do List Middleware

```python
todo_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[TodoListMiddleware()],
)
result = todo_agent.invoke({"messages": [("user",
    "I want to plan a movie night: check what's showing, pick something good, and book 2 seats.")]})
```

Gives a multi-step request an explicit, trackable plan instead of the model silently juggling several sub-tasks in one pass.

## 🎯 LLM Tool Selector — Fewer Tools, Cheaper Calls

```python
selector_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[
        LLMToolSelectorMiddleware(
            model="openai:gpt-5-mini",              # can be a CHEAPER model than the main agent
            max_tools=2,
            always_include=["check_showtimes"],      # always kept, doesn't count against max_tools
        ),
    ],
)
```

A small, separate model pre-filters which of CineBot's six tools are even relevant to a given message before the main agent call — genuinely cutting the token cost of sending every tool's full schema on every turn, the same "1,000 tools shouldn't all load for one request" problem raised the previous class.

## ⚠️ Tool Error Middleware — Controlling What the Model Sees on Failure

```python
def on_seat_error(exc: Exception, request) -> str | None:
    if isinstance(exc, ValueError):
        # Return the EXCEPTION TYPE, not str(exc) -- internal detail never reaches the model
        return f"`{request.tool_call['name']}` failed with {type(exc).__name__}. Please provide a valid seat number like 'A12'."
    return None  # anything else propagates and halts the run

error_handled_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[ToolErrorMiddleware(on_error=on_seat_error)],
)
```

Run against `lookup_seat_map`'s deliberately malformed-input `ValueError`, this turns a raw stack trace into a clean, actionable message the model can actually act on — without ever leaking internal exception text.

## 🔁 Tool Retry Middleware — Real Exponential Backoff

```python
@tool
def flaky_showtime_check(movie_title: str) -> str:
    """Check showtimes via an external service that can transiently fail."""
    if not random.random() > 1:   # deliberately always-true here, to force the failure path in the demo
        raise ConnectionError("Simulated network failure -- exactly what a real external call risks.")
    return f"{movie_title}: showing at 8:00 PM."

resilient_tool_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[flaky_showtime_check],
    middleware=[
        ToolRetryMiddleware(max_retries=3, backoff_factor=2.0, initial_delay=1.0, on_failure="continue"),
    ],
)
```

The exact backoff formula worked out live on the whiteboard:
```python
delay = initial_delay * backoff_factor ** retry_number
# retry 0: 1 * 2^0 = 1s
# retry 1: 1 * 2^1 = 2s
# retry 2: 1 * 2^2 = 4s
```
The Excalidraw board captions the same idea as **"Initial_Delay ="** next to **"4 (1 default and 3 retries)"** — 1 initial attempt plus 3 retries, 4 total tries, matching `max_retries=3` exactly. A second version of the tool, `flaky_showtime_check_time`, actually times and prints the real gap between calls (`time.time()`, `last_called`) to prove the backoff delay is genuinely growing, not just configured.

## 🎭 LLM Tool Emulator — Testing Without the Real Thing

```python
from langchain.agents.middleware import LLMToolEmulator

emulated_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[LLMToolEmulator(tools=["book_seats", "cancel_booking"], model="openai:gpt-5-mini")],
    # model= is passed EXPLICITLY here on purpose, not left to default
)
```

Lets specific tools be faked by a second model call instead of actually executing — useful for testing an agent's decision-making around a tool before the real integration (a real email send, a real payment) is safe to hit repeatedly in development.

## 🌍 Where These Patterns Show Up in Real Industries

Straight from the notebook's own real-world-mapping note:

> **Fraud detection in fintech:** a `wrap_tool_call`-style hook around every transaction-executing tool, flagging or blocking based on velocity, amount, or pattern.
> **Healthcare AI assistants:** `PIIMiddleware`-style redaction is often a genuine *legal* requirement (HIPAA in the US) — not optional polish.
> **Customer support platforms:** `HumanInTheLoopMiddleware`-style approval gates before any action with real financial consequence (refunds, account changes).
> **Internal developer tools:** audit logging via `wrap_tool_call` is close to universal anywhere "who did what, when" needs a real answer.

## 🕵️ Guardrail vs. Middleware — the Distinction That Keeps Coming Up

A **guardrail** is the concept — the goal of protecting an agent from doing something undesirable. **Middleware** is the mechanism used to actually implement that goal. The real whiteboard states this exactly: *"Guardrails is a way to control the AI agent behaviour"* — PII detection listed as one concrete instance of a guardrail, implemented via the `PIIMiddleware` mechanism above.

## ✅ Action Items

- [ ] 🔢 Set both a `run_limit` and a `thread_limit` on the same agent, and trigger each independently
- [ ] 🔀 Configure `ModelFallbackMiddleware` and force the primary model to fail (bad key) to confirm the fallback fires
- [ ] 🕵️ Write your own custom `PIIMiddleware` detector with `re` for an ID format relevant to your own country
- [ ] 🔁 Reproduce the exponential backoff demo and print the real elapsed time between retries
- [ ] 🎭 Try `LLMToolEmulator` on one of your own tools before wiring up the real integration

---
*Part of the [Live-Class-2026](../README.md) class summary index · ⬆️ [Weekend 07 overview](<../Weekend 07 - 8-9 Aug/README.md>). ⬅️ [Class 11](<11 - 01 Aug - Agents, Middleware & Memory.md>) · ➡️ [Class 13](<13 - 09 Aug - Guardrails, Todo Lists & Tool Resilience.md>)*
