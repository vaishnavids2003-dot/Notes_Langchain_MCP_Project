"""
02 -- THE EASY CLIENT
======================
The exact same five steps as 01_raw_client.py, but using fastmcp.Client
instead of building the three layers by hand. This is the version the
rest of this course has quietly been using the whole time, and it's the
safe choice to actually run live (it does not hit the macOS bug that
01_raw_client.py can).

SETUP:
    pip install fastmcp

RUN:
    python3 02_fastmcp_client.py
"""
import asyncio
from fastmcp import Client


async def main():
    # "Client(...)" replaces ALL of 01_raw_client.py's steps 1-3 at once:
    # it starts the subprocess, opens the streams, wraps the session, AND
    # does the handshake -- all inside this one "async with" block.
    async with Client("../main.py") as client:
        print("Connected! Handshake complete.")

        # Same as before: ask what's available
        tools = await client.list_tools()
        tool_names = [t.name for t in tools]
        print("Tools this server offers:", tool_names)

        # Same as before: call one for real
        result = await client.call_tool("list_projects", {})
        print("Result of calling list_projects:", result)


if __name__ == "__main__":
    asyncio.run(main())
