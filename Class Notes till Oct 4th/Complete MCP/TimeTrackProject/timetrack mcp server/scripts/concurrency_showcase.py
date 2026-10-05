"""
Concurrency + persistence showcase for a deployed TimeTrack MCP server.

Dev-only tool -- not part of the app, never deployed (see ../.gitignore).
Run it against the live server to see, with real timing evidence, the two
limitations the async-mysql upgrade (../../timetrack-async-mysql) fixes:

  1. Speedup: N calls run sequentially vs. N calls fired concurrently.
     A genuinely non-blocking/async server should approach an N x speedup;
     a sync server blocking on I/O will fall well short of it.
  2. Data integrity: after a concurrent burst, does every write actually
     show up on readback? A local SQLite file on a serverless host (e.g.
     Vercel) can lose everything once the function goes cold -- unrelated
     to sync vs async, but exactly why a real hosted database matters too.

Each call opens its own Client (its own MCP session/HTTP connection), so
the concurrency measured is the SERVER's, not an artifact of reusing one
session.

Usage:
    uv run scripts/concurrency_showcase.py
    TIMETRACK_MCP_URL=https://your-server/mcp/ uv run scripts/concurrency_showcase.py
    uv run scripts/concurrency_showcase.py --n 16
"""
import argparse
import asyncio
import os
import time
import uuid
from datetime import date

from fastmcp import Client

DEFAULT_URL = "https://time-track-server-iota.vercel.app/mcp/"
RUN_ID = uuid.uuid4().hex[:8]
TODAY = date.today().isoformat()


def employee_for(i: int) -> str:
    return f"ConcurrencyTest-{RUN_ID}-{i}"


async def timed_log_time(url: str, i: int, t0: float):
    start = time.perf_counter() - t0
    async with Client(url) as client:
        await client.call_tool("log_time", {
            "employee_name": employee_for(i),
            "project": "ConcurrencyShowcase",
            "entry_date": TODAY,
            "hours": round(1.0 + i * 0.01, 2),
            "description": f"concurrency-test run={RUN_ID} idx={i}",
        })
    end = time.perf_counter() - t0
    return i, start, end


async def verify(url: str, i: int):
    async with Client(url) as client:
        result = await client.call_tool("get_timesheet", {"employee_name": employee_for(i)})
    return i, result.data


async def main(url: str, n: int):
    print(f"Target server: {url}")
    print(f"Run ID: {RUN_ID}  |  N = {n} calls\n")

    print(f"=== Sequential baseline: {n} calls, one after another ===")
    t0 = time.perf_counter()
    for i in range(n):
        await timed_log_time(url, i, t0)
    seq_total = time.perf_counter() - t0
    print(f"Sequential total: {seq_total:.2f}s  (avg {seq_total / n:.2f}s/call)\n")

    print(f"=== Concurrent burst: {n} calls fired at once ===")
    t0 = time.perf_counter()
    conc_results = await asyncio.gather(*(timed_log_time(url, i + n, t0) for i in range(n)))
    conc_total = time.perf_counter() - t0
    print(f"Concurrent total: {conc_total:.2f}s\n")

    print("Timeline (each call's start->end in seconds since the burst began):")
    for i, start, end in sorted(conc_results, key=lambda r: r[1]):
        scale = 10
        bar_start = int(start * scale)
        bar_end = max(bar_start + 1, int(end * scale))
        print(f"  call {i:>2}: {'.' * bar_start}{'#' * (bar_end - bar_start)}  ({start:.2f}s -> {end:.2f}s)")

    speedup = seq_total / conc_total if conc_total else float("inf")
    print(f"\nSpeedup from concurrency: {speedup:.2f}x  (N={n}; a truly non-blocking server would approach {n}.0x)")
    if speedup < n * 0.5:
        print("=> Requests are largely SERIALIZING server-side, not running in parallel.")
    else:
        print("=> Requests overlapped well -- this deployment isn't showing the blocking limitation.")

    print("\n=== Data-integrity check: did every concurrent write actually persist? ===")
    checks = await asyncio.gather(*(verify(url, i + n) for i in range(n)))
    lost = [i for i, rows in checks if len(rows) == 0]
    if not lost:
        print(f"  All {n} concurrent writes persisted correctly.")
    else:
        print(f"  {len(lost)}/{n} entries are MISSING on readback: {[employee_for(i) for i in lost]}")
        print("  => Evidence of the local-SQLite-on-serverless problem (writes not surviving")
        print("     across container instances / cold starts).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=os.environ.get("TIMETRACK_MCP_URL", DEFAULT_URL),
                         help="MCP server URL to test (default: env TIMETRACK_MCP_URL, or the live Vercel deployment)")
    parser.add_argument("--n", type=int, default=int(os.environ.get("TIMETRACK_TEST_N", "8")),
                         help="number of calls per phase (default: 8)")
    args = parser.parse_args()
    asyncio.run(main(args.url, args.n))
