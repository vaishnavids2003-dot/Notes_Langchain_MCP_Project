"""
04 -- SAMPLING: THE SERVER BORROWS THE CLIENT'S LLM
=====================================================
main.py's "summarize_week" tool calls ctx.sample(...) internally. That
call does nothing on its own -- it PAUSES the tool and waits for
whichever client is connected to actually answer it. This file is the
client half: it provides the answer.

A NOTE WORTH KNOWING: as of the newest MCP spec revision, ctx.sample()
triggers a deprecation warning in your terminal. It still works -- this
is a live transition in the ecosystem (servers are moving toward calling
an LLM provider directly instead of borrowing the client's), not a
removal. You'll likely see the warning when you run this.

SETUP:
    pip install fastmcp anthropic
    export ANTHROPIC_API_KEY=your-key-here

RUN:
    python3 04_sampling_demo.py
"""
import asyncio
import os
from fastmcp import Client
from anthropic import Anthropic

anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


async def sampling_handler(messages, params, context) -> str:
    """
    This function is called BY the server, through the client, whenever
    a tool calls ctx.sample(). Whatever this function returns becomes the
    tool's result.
    """
    # "messages" is the prompt the server sent. Turn it into plain text.
    prompt_text = "\n".join(
        m.content.text if hasattr(m.content, "text") else str(m.content) for m in messages
    )

    # Now genuinely ask a real LLM -- this is the part that makes
    # sampling actually work, not just a stub.
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt_text}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


async def main():
    # Passing sampling_handler=... here is what "answers" any ctx.sample()
    # call the server makes while this client is connected.
    async with Client("../main.py", sampling_handler=sampling_handler) as client:
        result = await client.call_tool(
            "summarize_week",
            {"employee_name": "Asha Patel", "week_start": "2026-09-08"},
        )
        print("Summary, written by YOUR client's LLM, not the server:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
