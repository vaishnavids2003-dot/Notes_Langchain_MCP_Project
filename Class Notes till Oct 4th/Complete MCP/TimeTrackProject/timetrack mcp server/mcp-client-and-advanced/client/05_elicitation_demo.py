"""
05 -- ELICITATION: THE SERVER ASKS A REAL QUESTION
=====================================================
main.py's "log_time_with_confirmation" tool calls ctx.elicit(...)
whenever hours look unusually high. That call PAUSES the tool, mid-way
through, and waits for a real answer from the client. This file
provides that answer.

Unlike sampling, elicitation is NOT deprecated -- confirmed to survive
into the newest protocol revision.

SETUP:
    pip install fastmcp

RUN:
    python3 05_elicitation_demo.py
"""
import asyncio
from fastmcp import Client


async def elicitation_handler(message: str, response_type, params, context):
    """
    Called BY the server, through the client, whenever a tool calls
    ctx.elicit(). In a real app with a UI, this is where you'd show a
    real dialog box and wait for the person to click something. For this
    demo, we just print the question and auto-confirm.
    """
    print(f"\n[The server is asking]: {message}")
    print("[Auto-confirming for this demo -- swap this for real input() or a UI in your own client]")
    return True


async def main():
    async with Client("../main.py", elicitation_handler=elicitation_handler) as client:
        print("--- Logging 4 hours (normal -- watch: NO question gets asked) ---")
        normal_result = await client.call_tool(
            "log_time_with_confirmation",
            {"employee_name": "Asha Patel", "project": "Website Redesign",
             "entry_date": "2026-09-12", "hours": 4.0, "description": "A normal day"},
        )
        print("Result:", normal_result)

        print("\n--- Logging 14 hours (unusual -- watch: a real question appears) ---")
        high_result = await client.call_tool(
            "log_time_with_confirmation",
            {"employee_name": "Asha Patel", "project": "Website Redesign",
             "entry_date": "2026-09-12", "hours": 14.0, "description": "Crunch day"},
        )
        print("Result:", high_result)


if __name__ == "__main__":
    asyncio.run(main())
