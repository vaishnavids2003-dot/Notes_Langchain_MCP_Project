# 🤖 Class 11 — Agents, Middleware & Memory: Giving CineBot a Mind
### Agentic AI 3.0 Specialization | Live Class 2026

**🎙️ Mentor:** Mayank Aggarwal · **📅 Date:** 1 August 2026 · **⏱️ Duration:** ~4.5 hours

> 📂 **Code for this class:** [`11-12 - 1-8 Aug - Agents, Memory & Middleware/MIddleware.ipynb`](<../Weekend 06 - 1 Aug/11-12 - 1-8 Aug - Agents, Memory & Middleware/MIddleware.ipynb>) (cells 0–56) · [`Agent-Middleware-Architecture.excalidraw`](<../Weekend 06 - 1 Aug/11-12 - 1-8 Aug - Agents, Memory & Middleware/Agent-Middleware-Architecture.excalidraw>) — the real whiteboard, drawn live
> 🔗 Live Colab used in class: [Middleware notebook](https://colab.research.google.com/drive/1Qt9uU2HhDvtFTWwbbFBYxK86jJypv1w_?usp=sharing)

---

## 🎬 CineBot's Real Toolset for This Module

The notebook defines six genuinely reusable CineBot tools that every middleware demo below runs against:

```python
@tool
def check_showtimes(movie_title: str) -> str: ...
@tool
def book_seats(movie_title: str, seat_count: int) -> str:
    """Book seats for a movie. Irreversible once confirmed."""
    return f"Booked {seat_count} seat(s) for {movie_title}."
@tool
def cancel_booking(booking_id: str) -> str:
    """Cancel an existing booking. Irreversible."""
    return f"Booking {booking_id} cancelled."
@tool
def check_order_status(booking_id: str) -> str: ...
@tool
def get_refund_policy() -> str:
    """Get the cinema's refund policy -- exact wording, not to be paraphrased."""
    return "Refunds available up to 2 hours before showtime. No refunds after that."
@tool
def lookup_seat_map(movie_title: str, seat_number: str) -> str:
    """Look up a specific seat -- fails if the seat number format is wrong."""
    if not seat_number or not seat_number[0].isalpha():
        raise ValueError(f"Malformed seat number '{seat_number}' -- expected a letter+number like 'A12'.")
    return f"Seat {seat_number} for {movie_title}: available."

cinebot_tools = [check_showtimes, book_seats, cancel_booking, check_order_status, get_refund_policy, lookup_seat_map]
```

Note `book_seats` and `cancel_booking` are explicitly docstringed **"Irreversible"** — that word is doing real work; it's the exact property that makes them the tools worth gating with Human-in-the-Loop below.

## 🎛️ Middleware, Restated From the Real Whiteboard

The Excalidraw board drawn live in class captions the entire concept in one line: *"Middleware provides us a way to more tightly control what happens inside the agent."* Its loop diagram matches the code precisely:

```mermaid
flowchart LR
    A["📨 Request"] --> M1["before_agent"] --> M2["before_model"] --> M3["wrap_model_call"]
    M3 --> B["🧠 Model Call"] --> M4["after_model"] --> M5["wrap_tool_call"] --> C["🛠️ Tool Executes"]
    C --> M6["after_agent"] --> D["✅ Response"]

    style M2 fill:#f59e0b,color:#fff
    style M4 fill:#f59e0b,color:#fff
    style M5 fill:#f59e0b,color:#fff
```

The board also lists exactly what middleware is used for, four ways, matching the four demo categories this class and next actually build: *"Tracking agent behavior with logging, analytics, and debugging. Transforming prompts, tool selection, and output formatting. Adding retries, fallbacks, and early termination logic. Applying rate limits, guardrails, and PII detection."*

## 📝 Summarization Middleware — Real Config, Real Doc Note

```python
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[save_trip_demo],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",       # a separate, often cheaper model just for condensing
            trigger=("token", 4000),
            keep=("messages", 10),
        )
    ],
)
```

The real documentation note captured alongside it is worth keeping verbatim: *"Summarization is text-oriented context compression. It does not resize, downsample, or otherwise compress image/audio/video payloads. Recent messages retained by `keep` still include their original multimodal blocks, while older multimodal messages that are summarized are represented only by the generated text summary. For image-heavy applications, store media in a filesystem or object store and pass URLs or file references through message history."*

The whiteboard's own worked example: **4k tokens** triggers → *"Summarize the same"* → **100k ----> 10k tokens**, condensing a genuinely large real conversation down to a tenth of its size.

## ✋ Human-in-the-Loop — the Real Interrupt Diagram

Straight from the notebook's own markdown cell, the exact flow an interrupt takes:

```text
User
  │  "Send an email asking for leave"
  ▼
LLM
  │  decides to call
  ▼
your_send_email_tool
  │  requires approval
  ▼
INTERRUPT
  ├── approve → send email
  ├── edit    → modify tool arguments
  └── reject  → don't send
```

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

guarded_agent = create_agent(
    model="openai:gpt-5-mini",
    tools=cinebot_tools,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"cancel_booking": {"allowed_decisions": ["approve", "edit", "reject", "respond"]}}
        ),
    ],
    checkpointer=InMemorySaver(),  # REQUIRED -- HITL needs to pause and later resume
)
```

The whiteboard frames the whole idea with a real analogy: *"HITL middleware allows us to have a human oversight when an agent is calling a tool"* — drawn as **Request ---> Brain ----> Tool**, with a human standing exactly at that last arrow, captioned simply **"Intern."** An intern with a great brain still needs sign-off before doing something irreversible — that's the entire justification for where HITL sits in the loop.

**Resuming a paused agent, for real:**
```python
resumed_result = guarded_agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config,
)
```

The notebook builds this out into a genuinely interactive terminal demo, `run_interactive_hitl_demo()`, that reads a live typed decision — `approve` / `edit` / `reject` / `respond` — and applies it to the paused run in real time:

```python
def run_interactive_hitl_demo(agent, config):
    state = agent.get_state(config)
    if not state.next:
        print("Nothing is currently paused for approval.")
        return
    choice = input("Type 1, 2, 3, or 4: ").strip()
    if choice == "1":
        decision = {"type": "approve"}
    elif choice == "2":
        new_id = input("New booking_id to use instead: ").strip()
        decision = {"type": "edit", "args": {"booking_id": new_id}}
    elif choice == "3":
        reason = input("Reason for rejecting: ").strip()
        decision = {"type": "reject", "message": reason}
    elif choice == "4":
        answer = input("Your response to the agent: ").strip()
        decision = {"type": "respond", "message": answer}
    resumed = agent.invoke(Command(resume={"decisions": [decision]}), config=config)
    print("Agent's final response:", resumed["messages"][-1].content)
```

> ⚙️ **From the real code walkthrough note:** *"`Command(resume={"decisions": [...]})` is how you hand a decision back to an agent that's paused mid-run. The `decisions` list has one entry per interrupted tool call (usually just one). Each decision is a dict with a `"type"` key matching one of the four options, plus whatever extra data that type needs — `edit` needs new `args`, `reject` and `respond` need a `message`, `approve` needs nothing else."*

## 🗄️ Memory — the Whiteboard's "Empty & Nothing Remembered" Demo

The Excalidraw board captures this class's memory demo as a direct before/after comparison, literally labeled on the drawing: **"without in memory saver"** — `invoke → result → invoke2` → **"Empty & Nothing Remembered"** — versus **"with in memory saver"** — `invoke → result → invoke2` → *"it has all the Previous messages."* The fix is the same `InMemorySaver` + `thread_id` pattern used throughout the rest of the course:

```python
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
agent_with_memory = create_agent(model=model, tools=[...], checkpointer=checkpointer)
config = {"configurable": {"thread_id": "mayank-session-1"}}
```

## ✅ Action Items

- [ ] 📝 Recreate `SummarizationMiddleware` with your own `trigger`/`keep`, and watch a long conversation actually compress
- [ ] ✋ Build the `cancel_booking` HITL demo, then run `run_interactive_hitl_demo()` yourself and try all four decision types
- [ ] 🗄️ Reproduce the whiteboard's own before/after: two `invoke()` calls with no checkpointer, then the same two calls with `InMemorySaver()` + a fixed `thread_id`
- [ ] 🎨 Open [`Agent-Middleware-Architecture.excalidraw`](<../Weekend 06 - 1 Aug/11-12 - 1-8 Aug - Agents, Memory & Middleware/Agent-Middleware-Architecture.excalidraw>) in [excalidraw.com](https://excalidraw.com) and trace the full loop diagram by hand

---

## ➡️ Up Next
**[Class 12 — 8 Aug — Mastering Middleware »](<12 - 08 Aug - Mastering Middleware.md>)**

---
*Part of the [Live-Class-2026](../README.md) class summary index · ⬆️ [Weekend 06 overview](<../Weekend 06 - 1 Aug/README.md>). ⬅️ [Class 10](<10 - 26 Jul - Tools Deep Dive.md>)*
