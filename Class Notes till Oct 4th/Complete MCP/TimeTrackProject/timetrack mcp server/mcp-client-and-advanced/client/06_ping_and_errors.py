"""
06 -- PING AND A REAL ERROR
=============================
Two of the "special cases" from the Lifecycle video, now actually
happening instead of being a JSON example on a slide.

RUN:
    python3 06_ping_and_errors.py
"""
import asyncio
from fastmcp import Client


async def demo_ping():
    print("--- PING: just checking the connection is alive ---")
    async with Client("../main.py") as client:
        result = await client.ping()
        print("Server responded:", result)


async def demo_real_error():
    print("\n--- A REAL ERROR, TRIGGERED ON PURPOSE ---")
    async with Client("../main.py") as client:
        try:
            # "Nonexistent Project" was never logged against -- this makes
            # get_project_summary's own ValueError fire for real, and
            # surface back to us as a genuine protocol error.
            await client.call_tool("get_project_summary", {"project": "Nonexistent Project"})
        except Exception as e:
            print("Caught a real error response:", e)


async def main():
    await demo_ping()
    await demo_real_error()


if __name__ == "__main__":
    asyncio.run(main())
