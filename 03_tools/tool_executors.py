"""Tool executors — control how parallel tool calls are dispatched.

When the model emits multiple tool calls in a single turn, the agent's
tool_executor decides whether they run in parallel or one at a time.

  ConcurrentToolExecutor (default): runs all tool calls in parallel.
                                    Fastest, but the tools must be safe to
                                    interleave (no shared mutable state).
  SequentialToolExecutor:           runs tool calls one after the other in
                                    the order the model emitted them. Use when
                                    tools share state, mutate the same file,
                                    or must observe a strict ordering.
"""

import time
from strands import Agent, tool
from strands.tools.executors import SequentialToolExecutor


@tool
def slow_lookup(key: str) -> str:
    """Look up a value (deliberately slow)."""
    time.sleep(1)
    return f"value-for-{key}"


# Sequential — three slow_lookup calls take ~3s total.
agent_seq = Agent(tools=[slow_lookup], tool_executor=SequentialToolExecutor())

# Concurrent (default) — three slow_lookup calls take ~1s total.
agent_par = Agent(tools=[slow_lookup])


if __name__ == "__main__":
    prompt = "Look up keys 'a', 'b', and 'c' and report all three values."

    t0 = time.monotonic()
    agent_seq(prompt)
    print(f"\nSequential: {time.monotonic() - t0:.2f}s\n")

    t0 = time.monotonic()
    agent_par(prompt)
    print(f"\nConcurrent: {time.monotonic() - t0:.2f}s")
