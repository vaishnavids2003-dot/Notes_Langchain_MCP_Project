# 🧠 Class 08 — Inside the Model: Environment, Messages, Streaming & Tool Binding
### Agentic AI 3.0 Specialization | Live Class 2026

**🎙️ Mentor:** Mayank Aggarwal · **📅 Date:** 19 July 2026 · **⏱️ Duration:** ~4.5 hours

> 📂 **Code for this class:** [`07-08 - 18-19 Jul - LangChain Family & the Model Layer/Notebook For Reference/02_03_environment_models_messages_student_notes.ipynb`](<../Weekend 04 - 18-19 Jul/07-08 - 18-19 Jul - LangChain Family & the Model Layer/Notebook For Reference/02_03_environment_models_messages_student_notes.ipynb>)
> 🔗 Live Colabs used in class: [Live session notebook](https://colab.research.google.com/drive/16yT0w6ha6eWK2dOHsOrj7qW8oZiIvGxc?usp=sharing) · [Revision Notebook — Parts 1-4](https://colab.research.google.com/drive/1v15iHbt8lsIRsPYw0UgSOCogaenBo4_W?usp=sharing)

---

## 🔐 Where Your API Key Actually Lives

The real notebook is blunt about this, and it's worth repeating verbatim: *"if `.env` isn't listed in `.gitignore`, the very first time you commit and push your code, your real API key gets uploaded to GitHub along with it — where it can be found and used by anyone, often within minutes, by automated scanners that specifically look for leaked keys."*

```python
import os
from dotenv import load_dotenv
load_dotenv()
assert os.environ.get("OPENAI_API_KEY"), "Missing OPENAI_API_KEY -- check your .env file"
```

**If this throws an auth error:** either `.env` isn't in the folder you're running from, or you created it *after* starting the notebook session — restart the kernel so `load_dotenv()` picks up the file that now exists.

## 🧬 What You Actually Get Back: the Full `AIMessage`

This is the section the real notebook flags as *"most tutorials skip entirely."* Every model call returns an object with far more than the text reply:

| Field | What it holds |
|---|---|
| `.text` | The plain text reply, always a string |
| `.content` / `.content_blocks` | Raw content, or LangChain's standardized rich-content structure (text, reasoning, citations, images) |
| `.tool_calls` | Any tool calls requested — empty list if none |
| `.id` | A unique identifier for this message |
| `.usage_metadata` | Real token counts: `input_tokens`, `output_tokens`, `total_tokens` |
| `.response_metadata` | Provider-specific extras — which exact model responded, why it stopped generating |

```python
response = openai_model.invoke("Explain agentic AI in one sentence.")
print("text:          ", response.text)
print("tool_calls:    ", response.tool_calls)   # empty -- no tools bound yet
print(response.usage_metadata)
# {'input_tokens': ..., 'output_tokens': ..., 'total_tokens': ...,
#  'input_token_details': {...}, 'output_token_details': {...}}
```

**You do not need a separate token-counting library.** The exact billed numbers are already sitting on the response.

## 📡 Streaming: `AIMessageChunk` Objects That Sum With `+`

```python
chunks = []
full_message = None
for chunk in openai_model.stream("Write one short sentence about the ocean."):
    chunks.append(chunk)
    full_message = chunk if full_message is None else full_message + chunk

print("Reconstructed full message:", full_message.content)
# Never called .invoke() -- the full message was built purely by summing chunks,
# and it comes out identical in shape to what .invoke() would have given.
```

## 🛠️ Tool Binding — Preview

```python
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"Sunny in {location}"

model_with_tools = openai_model.bind_tools([get_weather])   # AWARE, does not execute
response = model_with_tools.invoke("What's the weather in Paris?")
for tool_call in response.tool_calls:
    print(f"Tool: {tool_call['name']}  Args: {tool_call['args']}  ID: {tool_call['id']}")
```

## 📤 `ToolMessage` and `.artifact`: Two Audiences for One Result

```python
from langchain_core.messages import ToolMessage

tool_message = ToolMessage(
    content="It was the best of times, it was the worst of times.",
    tool_call_id="call_123",
    name="search_books",
    artifact={"document_id": "doc_123", "page": 0},   # the MODEL never sees this
)
print("What the MODEL sees:", tool_message.content)
print("What your APP can use:", tool_message.artifact)
```

This matters when a tool needs to hand back more than the model needs — a retrieval tool returning the passage as `.content` (for the model) while attaching a document ID as `.artifact` (for your app to build a citation link with, later).

## ⚖️ Paid vs. Free/Local — One String Changes

```python
paid_model = init_chat_model("openai:gpt-5-mini")

# free_model = init_chat_model("ollama:llama3.2")   # runs entirely on your own machine, no API key
# response = free_model.invoke("In one sentence, what is LangChain?")
```

**Honest caveat from the notes:** free/local models are genuinely free of API cost, but not of hardware cost — `llama3.2` needs real RAM (ideally a GPU) to run at usable speed, and response quality noticeably trails a frontier paid model. Same interface, different intelligence underneath.

## 💬 Manually Inserting History — Legitimately vs. Dishonestly

```python
ai_msg = AIMessage("I'd be happy to help you with that question!")
messages = [SystemMessage("You are a helpful assistant"), HumanMessage("Can you help me?"),
            ai_msg,   # inserted directly -- the model never actually generated this
            HumanMessage("Great! What's 2+2?")]
```

**Important distinction from the real notes:** this is legitimate for restoring real conversation history — it is *not* a way to make the model "believe" it agreed to something for the current turn in a way that biases its behavior dishonestly, since the model treats a fabricated `AIMessage` as real context either way.

## 📝 Prompt Templates — Writing the Structure Once

> 📂 Continues in [`04_05_prompt_templates_structured_output_student_notes.ipynb`](<../Weekend 04 - 18-19 Jul/07-08 - 18-19 Jul - LangChain Family & the Model Layer/Notebook For Reference/04_05_prompt_templates_structured_output_student_notes.ipynb>)

An f-string prompt works for one case; the moment you need the same structure with different tones or multiple variables, you're rewriting it by hand every time, with no warning on a silent typo. `ChatPromptTemplate` separates the fixed structure from what actually changes:

```python
from langchain_core.prompts import ChatPromptTemplate

fun_fact_prompt = ChatPromptTemplate.from_messages([
    ("system", "You generate a single surprising fun fact. Tone: {tone}."),
    ("human", "Topic: {topic}"),
])

chain = fun_fact_prompt | openai_model   # the | pipe feeds the template's OUTPUT into the model's INPUT

for tone, topic in [("playful and silly", "octopuses"), ("deadpan and serious", "octopuses")]:
    result = chain.invoke({"tone": tone, "topic": topic})
    print(f"[{tone} / {topic}] -> {result.content}")
```

Same underlying structure across every call — only the two variables change, yet the two "octopuses" outputs sound completely different because of `tone` alone.

## 📐 Structured Output — the Problem, Proven Live

Three real, differently-phrased customer messages sent through plain-text extraction:

```python
messages = [
    "Hi, I'm Rina, my order arrived broken and I need a refund ASAP.",
    "hey its dave, package never showed up, kinda annoyed tbh",
    "This is Comfort. My item was fine but delivery took 3 weeks - just flagging it, not urgent.",
]
for msg in messages:
    r = openai_model.invoke(f"Extract the customer's name and issue from: {msg}")
    print(r.content)
```

No two replies are guaranteed to share a shape — one might read "Name: Rina, Issue: broken order," another a full sentence. **Free text isn't wrong. It's just not a contract.**

```python
from pydantic import BaseModel, Field
from typing import Literal

class SupportTicket(BaseModel):
    customer_name: str = Field(description="The customer's first name")
    issue_category: Literal["refund", "delivery", "product_defect", "other"]   # closed set -- can't invent a 5th
    urgency: Literal["low", "medium", "high"]
    needs_human: bool = Field(description="True if this needs a human agent, not a bot")

structured_model = openai_model.with_structured_output(SupportTicket)
for msg in messages:
    print(structured_model.invoke(f"Extract a support ticket from this message: {msg}"))
```

Same three messy inputs, same underlying model — the only change is handing it a schema first. Every result now comes back as the exact same `SupportTicket` object.

**Pydantic `BaseModel` vs. `TypedDict`:** `BaseModel` validates every field strictly and rejects/retries on mismatch; `TypedDict` defines the same shape with **no validation at all** — faster and lighter, but nothing stops a malformed result getting through. Default to Pydantic when correctness genuinely matters.

**`ProviderStrategy` vs. `ToolStrategy`:** `ProviderStrategy` uses the provider's own native structured-output feature (fast, only where supported); `ToolStrategy` fakes it via a synthetic tool call (works almost anywhere, slightly more overhead). LangChain auto-selects unless you force one — pass a bare schema and it picks for you.

⚠️ **An honest caveat straight from the notes:** there are documented, community-reported cases (late 2025) where `ToolStrategy` combined with *real* tool calls in the same agent behaves unreliably on certain models — hitting recursion limits or failing to execute correctly. Test your specific model and use case before trusting the combination for anything important.

## ✅ Action Items

- [ ] ⚙️ Print `.usage_metadata` on a real call and confirm it matches your provider's dashboard
- [ ] 📡 Run the streaming example and confirm `full_message.content` matches what `.invoke()` would return
- [ ] 🛠️ `bind_tools()` on a function, `.invoke()`, inspect `response.tool_calls` — remember, nothing executes yet
- [ ] 📤 Build a `ToolMessage` with a real `.artifact` and confirm the model output never mentions it
- [ ] ⚖️ If you have the RAM, install Ollama and run the same prompt through a local model — compare quality against the paid one

---

## ➡️ Up Next
**[Class 09 — 25 Jul — Structured Output Mastery: Building CineBot »](<09 - 25 Jul - Structured Output Mastery.md>)**
📂 Code folder: [`09-10 - 25-26 Jul - Structured Output & Tools (CineBot)/`](<../Weekend 05 - 25-26 Jul/09-10 - 25-26 Jul - Structured Output & Tools (CineBot)/>)

---
*Part of the [Live-Class-2026](../README.md) class summary index · ⬆️ [Weekend 04 overview](<../Weekend 04 - 18-19 Jul/README.md>). ⬅️ [Class 07](<07 - 18 Jul - LangChain Family & Harness Engineering.md>)*
