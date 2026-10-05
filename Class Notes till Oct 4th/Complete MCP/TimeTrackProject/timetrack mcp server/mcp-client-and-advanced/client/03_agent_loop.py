"""
03 -- A REAL AGENT LOOP, NO FRAMEWORK
=======================================
This is what "an AI agent using MCP" actually is, underneath every
framework that promises to do it for you. No LangChain, nothing hidden --
just: ask the LLM, check if it wants a tool, call it for real through
MCP, hand the result back, repeat.

SETUP:
    pip install fastmcp anthropic
    export ANTHROPIC_API_KEY=your-key-here

RUN:
    python3 03_agent_loop.py
"""
import asyncio
import os
from fastmcp import Client
from anthropic import Anthropic


def mcp_tools_to_anthropic_format(mcp_tools) -> list[dict]:
    """
    MCP describes a tool one way. Anthropic's API wants it described a
    slightly different way. This is the ONLY translation a framework-free
    agent loop actually needs to do by hand.
    """
    return [
        {
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": tool.inputSchema,
        }
        for tool in mcp_tools
    ]


async def run_one_tool_call(mcp_client: Client, block) -> dict:
    """Actually calls one tool through MCP, and packages the result the
    way Anthropic's API expects it to come back."""
    print(f"  -> calling {block.name} with {block.input}")
    result = await mcp_client.call_tool(block.name, block.input)
    return {
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": str(result),
    }


async def run_agent_loop(user_message: str):
    anthropic_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    async with Client("../main.py") as mcp_client:
        mcp_tools = await mcp_client.list_tools()
        anthropic_tools = mcp_tools_to_anthropic_format(mcp_tools)

        # This list is the entire "memory" of the conversation. Every
        # question, every tool result, gets appended here and sent back
        # on the NEXT request -- the LLM itself remembers nothing between
        # calls; this list is doing all the remembering.
        messages = [{"role": "user", "content": user_message}]

        while True:
            response = anthropic_client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                tools=anthropic_tools,
                messages=messages,
            )

            if response.stop_reason != "tool_use":
                # The model is done -- it answered in plain text. Print it
                # and stop the loop.
                final_text = "".join(
                    block.text for block in response.content if block.type == "text"
                )
                print("\nFinal answer:", final_text)
                return

            # The model wants to use one or more tools. Save its request
            # to the conversation, then actually go run each tool call.
            messages.append({"role": "assistant", "content": response.content})

            tool_results = [
                await run_one_tool_call(mcp_client, block)
                for block in response.content
                if block.type == "tool_use"
            ]

            # Feed the results back in as the next "turn", and loop again --
            # the model will see these results the next time we call it.
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    asyncio.run(run_agent_loop(
        "List every project in TimeTrack, then give me the summary for the first one."
    ))
