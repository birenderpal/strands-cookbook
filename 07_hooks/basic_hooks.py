"""Hooks let you intercept agent lifecycle events."""

from strands import Agent, tool
from strands.agent.hooks import (
    BeforeModelCallEvent,
    AfterModelCallEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
)


@tool
def get_time():
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")


def on_before_model(event: BeforeModelCallEvent):
    print(f"-> Calling model with {len(event.messages)} messages")


def on_after_model(event: AfterModelCallEvent):
    tokens = event.usage.get("totalTokens", 0) if event.usage else 0
    print(f"<- Model responded ({tokens} tokens)")


def on_before_tool(event: BeforeToolCallEvent):
    print(f"-> Calling tool: {event.tool_use.get('name')}")
    # event.cancel_tool = True  # uncomment to block tool execution


def on_after_tool(event: AfterToolCallEvent):
    print(f"<- Tool done: {event.tool.tool_name}")


agent = Agent(
    tools=[get_time],
    hooks={
        BeforeModelCallEvent: on_before_model,
        AfterModelCallEvent: on_after_model,
        BeforeToolCallEvent: on_before_tool,
        AfterToolCallEvent: on_after_tool,
    }
)


if __name__ == "__main__":
    agent("What time is it?")
