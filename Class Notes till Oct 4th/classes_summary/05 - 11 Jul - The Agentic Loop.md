# 🔁 Class 05 — Building Real Agents in Pure Python: The Agentic Loop
### Agentic AI 3.0 Specialization | Live Class 2026

**🎙️ Mentor:** Mayank Aggarwal · **📅 Date:** 11 July 2026 · **⏱️ Duration:** ~4.5 hours

> 📂 **Code for this class:** [`04-05 - 5 Jul & 11 Jul - Anatomy of an Agent & The Agentic Loop/Project 0/`](<../Weekend 02 - 4-5 Jul/04-05 - 5 Jul & 11 Jul - Anatomy of an Agent & The Agentic Loop/Project 0/>) — files `_05`–`_07`, finishing **Project Zero**

---

> *"I know I would have started with LangChain to make everyone happy — but now you'll actually **appreciate** LangChain instead of just copy-pasting it."*

## 🧠 Letting the Model Choose a Tool — the Real Schema

[`_05_teaching_it_to_choose.py`](<../Weekend 02 - 4-5 Jul/04-05 - 5 Jul & 11 Jul - Anatomy of an Agent & The Agentic Loop/Project 0/_05_teaching_it_to_choose.py>) hands the model a genuine "menu" of tool schemas — not the function itself, only its description:

```python
get_weather_schema = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city. Use this whenever "
                        "the user asks about weather, temperature, or conditions "
                        "in a specific place. Don't use it for AQI",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "The city name, e.g. 'Tokyo'."}},
            "required": ["city"],
        },
    },
}

def ask_ai_to_choose(question: str):
    client, model = get_client_and_model()
    response = client.chat.completions.create(
        model=model, max_tokens=300,
        messages=[{"role": "user", "content": question}],
        tools=[get_weather_schema, get_capital_schema, get_tool_schema_for_llm],
    )
    return response.choices[0].message
```

The file keeps its own real transcript from class, in a comment block — genuinely useful as a reference for what the raw response object looks like:

```text
what is the weather like in Tokyo right now?

Model's raw reply: ChatCompletionMessage(content=None, ..., tool_calls=
[ChatCompletionMessageToolCall(id='call_x4l82u...', function=Function(
    arguments='{"city":"Tokyo"}', name='get_weather'), type='function')])

What is the capital of Japan?
Model's raw reply: ...tool_calls=[
    ChatCompletionMessageToolCall(..., function=Function(arguments='{"country":"Japan"}', name='get_capital')),
    ChatCompletionMessageToolCall(..., function=Function(arguments='{"country":"Tokyo"}', name='get_capital')),
    ChatCompletionMessageToolCall(..., function=Function(arguments='{"country":"Delhi"}', name='get_capital'))]
```

That second example is a genuinely useful, slightly messy real result: a single question triggered **three separate tool calls at once** — live proof that a model can request more than one tool call in a single reply, not just one.

## 🔁 The Agentic Loop, Assembled

[`_06_project_zero_agent.py`](<../Weekend 02 - 4-5 Jul/04-05 - 5 Jul & 11 Jul - Anatomy of an Agent & The Agentic Loop/Project 0/_06_project_zero_agent.py>) is where every previous file's pattern locks together into the real loop:

```python
def run_agent(messages: list, max_turns: int = 4) -> str:
    """Each turn: call the model with the tool schema attached; if it replies with
    tool_calls, execute every one of them and feed the results back in; if it
    replies with plain content instead, that is the final answer and the loop stops."""
    client, model = get_client_and_model()

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=model, max_tokens=300, messages=messages, tools=TOOL_SCHEMAS
        )
        message = response.choices[0].message

        if not message.tool_calls:
            messages.append({"role": "assistant", "content": message.content})
            return message.content

        messages.append({
            "role": "assistant", "content": message.content,
            "tool_calls": [{"id": call.id, "type": "function",
                             "function": {"name": call.function.name, "arguments": call.function.arguments}}
                            for call in message.tool_calls],
        })

        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments)
            tool_function = TOOLS_BY_NAME[call.function.name]
            result = tool_function(**arguments)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})

    return "Reached max_turns without a final answer."
```

Wrapped in a minimal terminal REPL where `conversation_memory` — a single growing Python list — **is** the agent's entire memory:

```python
def chat() -> None:
    conversation_memory: list[dict] = []
    while True:
        user_input = input("You: ")
        conversation_memory.append({"role": "user", "content": user_input})
        answer = run_agent(conversation_memory)
        print(f"Agent: {answer}\n")
```

## 🎨 The Streamlit Front End — Three Real Tools

[`_07_streamlit_app.py`](<../Weekend 02 - 4-5 Jul/04-05 - 5 Jul & 11 Jul - Anatomy of an Agent & The Agentic Loop/Project 0/_07_streamlit_app.py>) is the same `run_agent` loop, now driving a real chat UI with three tools registered — weather (mock data), a sandboxed `calculator`, and **live** currency conversion via the Frankfurter API:

```python
def calculator(expression: str) -> str:
    """Only digits, operators, and parentheses are allowed through before eval() ever runs,
    so arbitrary code can't be smuggled in via the expression string."""
    allowed_characters = set("0123456789+-*/(). ")
    if not set(expression) <= allowed_characters:
        return f"Rejected -- expression contains disallowed characters: {expression!r}"
    return str(eval(expression))

# st.session_state.messages is this app's memory -- it survives Streamlit's
# re-runs on every interaction, which a plain local variable would not.
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask about the weather, do some maths, or convert a currency...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = run_agent(st.session_state.messages)
        st.write(answer)
```

## 🧩 Why the Loop Runs *Again* After a Tool Call

The AI is called again after a tool runs because it never automatically "knows" the tool's output — that result has to be explicitly fed back in as a new message before the model can use it to form a final answer. `max_turns` caps runaway loops.

## ✅ Action Items

- [ ] 🐍 Run `_05` yourself and deliberately ask a question that could trigger two tools at once — inspect `message.tool_calls`
- [ ] 🔁 Step through `_06`'s `run_agent` loop by hand, tracing exactly what gets appended to `messages` on a tool-call turn vs. a final-answer turn
- [ ] 🎨 Run `uv run streamlit run _07_streamlit_app.py` and try all three tools in one conversation
- [ ] 🧠 Explain, unprompted, why the loop re-calls the AI after a tool executes

---

## ➡️ Up Next
**[Class 06 — 12 Jul — Introduction to LangChain »](<06 - 12 Jul - Introduction to LangChain.md>)**
📂 Code folder: [`06 - 12 Jul - Introduction to LangChain/`](<../Weekend 03 - 11-12 Jul/06 - 12 Jul - Introduction to LangChain/>)

---
*Part of the [Live-Class-2026](../README.md) class summary index · ⬆️ [Weekend 03 overview](<../Weekend 03 - 11-12 Jul/README.md>). ⬅️ [Class 04](<04 - 5 Jul - Anatomy of an Agent.md>)*
