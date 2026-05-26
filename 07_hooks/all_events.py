"""All single-agent lifecycle events in one place.

Order during a single `agent("...")` call:
    AgentInitializedEvent       (once, at Agent construction time)
    BeforeInvocationEvent       (per user request)
        MessageAddedEvent       (user message added)
        BeforeModelCallEvent
        AfterModelCallEvent
        MessageAddedEvent       (assistant message added)
        BeforeToolCallEvent     (only if the model called a tool)
        AfterToolCallEvent
        ... repeats until no more tool calls ...
    AfterInvocationEvent

Multi-agent orchestrators emit BeforeNodeCallEvent / AfterNodeCallEvent and
their own Before/After*MultiAgentInvocationEvent — see graph_basic.py / swarm_basic.py.
"""

from strands import Agent, tool
from strands.hooks import (
    AgentInitializedEvent,
    BeforeInvocationEvent,
    AfterInvocationEvent,
    MessageAddedEvent,
    BeforeModelCallEvent,
    AfterModelCallEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
)


@tool
def echo(text: str) -> str:
    """Echo back the given text."""
    return text


def on_init(event: AgentInitializedEvent) -> None:
    print(f"[init] {event.agent.name}")


def on_before_invoke(event: BeforeInvocationEvent) -> None:
    print("[invoke:start]")
    # event.messages = ...  # rewrite/redact the input messages here


def on_after_invoke(event: AfterInvocationEvent) -> None:
    print("[invoke:end]")
    # event.resume = "continue"  # re-invoke the agent automatically (autonomous loop)


def on_message(event: MessageAddedEvent) -> None:
    print(f"[message] role={event.message['role']}")


def on_before_model(event: BeforeModelCallEvent) -> None:
    print("[model:before]")


def on_after_model(event: AfterModelCallEvent) -> None:
    print("[model:after]")
    # event.retry = True  # discard response and call the model again


def on_before_tool(event: BeforeToolCallEvent) -> None:
    print(f"[tool:before] {event.tool_use['name']}")


def on_after_tool(event: AfterToolCallEvent) -> None:
    print(f"[tool:after] {event.tool_use['name']}")


agent = Agent(
    tools=[echo],
    hooks=[
        on_init,
        on_before_invoke,
        on_message,
        on_before_model,
        on_after_model,
        on_before_tool,
        on_after_tool,
        on_after_invoke,
    ],
)


if __name__ == "__main__":
    agent("Use the echo tool with the text 'hello'.")
