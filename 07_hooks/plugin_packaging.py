"""Plugins — package hooks + tools together as reusable, stateful units.

A Plugin auto-discovers methods decorated with @hook and @tool when constructed,
then attaches them to any agent it's passed to. Use this over a bare callback list
when you want:
  - shared state across multiple hook events (e.g. a request counter)
  - hooks + tools shipped as one unit (e.g. an auth plugin that adds a token tool
    AND signs every model call)
  - distributable, importable behavior packs

For one-shot, stateless hooks, the list form in basic_hooks.py is simpler.
"""

import time
from strands import Agent, tool
from strands.hooks import BeforeInvocationEvent, AfterInvocationEvent, BeforeToolCallEvent
from strands.plugins import Plugin, hook


class TimingPlugin(Plugin):
    """Tracks per-invocation latency and exposes a tool that reports the stats."""

    name = "timing"

    def __init__(self) -> None:
        super().__init__()
        self._started_at: float | None = None
        self._invocations: list[float] = []
        self._tool_calls = 0

    @hook
    def on_start(self, event: BeforeInvocationEvent) -> None:
        self._started_at = time.monotonic()

    @hook
    def on_tool(self, event: BeforeToolCallEvent) -> None:
        self._tool_calls += 1

    @hook
    def on_end(self, event: AfterInvocationEvent) -> None:
        if self._started_at is not None:
            self._invocations.append(time.monotonic() - self._started_at)
            self._started_at = None

    @tool
    def get_timing_stats(self) -> str:
        """Get latency stats from the timing plugin."""
        if not self._invocations:
            return "No invocations recorded yet."
        avg = sum(self._invocations) / len(self._invocations)
        return (
            f"{len(self._invocations)} invocations, "
            f"avg {avg:.2f}s, "
            f"{self._tool_calls} tool calls total"
        )


agent = Agent(plugins=[TimingPlugin()])


if __name__ == "__main__":
    agent("What is 1 + 1?")
    agent("What is 2 + 2?")
    agent("Call get_timing_stats and report what it returns.")
