"""Hooks let you intercept agent lifecycle events.

Pass plain callables to `hooks=[...]` — the event type is inferred from the
first parameter's type annotation. For stateful or multi-event setups, use a
HookProvider (see plugin_packaging.py).
"""

from strands import Agent, tool
from strands.hooks import (
    BeforeModelCallEvent,
    AfterModelCallEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
)


@tool
def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")


def on_before_model(event: BeforeModelCallEvent) -> None:
    print(f"-> Calling model (projected input tokens: {event.projected_input_tokens})")


def on_after_model(event: AfterModelCallEvent) -> None:
    stop = event.stop_response.stop_reason if event.stop_response else "error"
    print(f"<- Model done (stop_reason={stop})")


def on_before_tool(event: BeforeToolCallEvent) -> None:
    print(f"-> Calling tool: {event.tool_use['name']}")
    # event.cancel_tool = True   # cancel and surface as an error tool result
    # event.cancel_tool = "..."  # cancel with a custom message


def on_after_tool(event: AfterToolCallEvent) -> None:
    print(f"<- Tool done: {event.tool_use['name']}")
    # event.retry = True  # discard the current result and call the tool again


agent = Agent(
    tools=[get_time],
    hooks=[on_before_model, on_after_model, on_before_tool, on_after_tool],
)


if __name__ == "__main__":
    agent("What time is it?")
