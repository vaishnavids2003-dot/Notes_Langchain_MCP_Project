# Project Zero

Built across **[Class 04](<../../../classes_summary/04 - 5 Jul - Anatomy of an Agent.md>)** and **[Class 05](<../../../classes_summary/05 - 11 Jul - The Agentic Loop.md>)** (5 & 11 July 2026) — the raw-Python agent, from first principles to a full agentic loop with a UI.

| File | Contents |
|---|---|
| `_01_ai_model_vs_chatbot_vs_agent.py` | Structural comparison of the three, no API calls |
| `_02_calling_the_ai_paid_and_free.py` | Real API calls: OpenAI, Anthropic, Groq, OpenRouter |
| `_03_structuring_with_pydantic.py` | Structured JSON extraction, validated with Pydantic |
| `_04_giving_it_a_tool.py` | A weather tool, called manually |
| `_05_teaching_it_to_choose.py` | Tool schema + the model choosing and calling the tool itself |
| `_06_project_zero_agent.py` | The full loop, terminal chat, one tool |
| `_07_streamlit_app.py` | The full loop with a Streamlit front end, three tools (weather, calculator, currency) |

Each file is independent and can be run on its own. All files require a real API key --
there is no offline stand-in.

## Setup

```bash
uv sync
cp .env.example .env
# fill in at least one key -- GROQ_API_KEY is free and fastest to get
```

## Run

```bash
uv run _01_ai_model_vs_chatbot_vs_agent.py
uv run streamlit run _07_streamlit_app.py
```
