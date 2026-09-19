"""Steering — Guide-and-Proceed safety pattern.

Steering inserts a decision point before each tool call (and after each model
response). For every tool call the handler returns one of:

  Proceed   — let the tool run as planned
  Guide     — cancel the tool and feed the reason back to the model so it can
              try a different approach (no human in the loop)
  Interrupt — pause execution and request human input via the interrupt system

Use this when you want graduated control beyond pre-flight guardrails:
  - block specific high-risk arguments (this file)
  - require approval for irreversible ops (return Interrupt)
  - nudge the agent toward cheaper or safer alternatives without hard-stopping

For LLM-based steering with natural-language rules, use LLMSteeringHandler.
"""

from typing import Any
from strands import Agent, tool
from strands.types.tools import ToolUse
from strands.vended_plugins.steering import (
    Guide,
    Interrupt,
    Proceed,
    SteeringHandler,
    ToolSteeringAction,
)


@tool
def delete_user(user_id: str) -> str:
    """Delete a user account."""
    return f"User {user_id} deleted."


@tool
def send_email(to: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {to}."


class PolicyHandler(SteeringHandler):
    """Policy-based steering: redirect risky tool calls, escalate destructive ones."""

    name = "policy"

    async def steer_before_tool(
        self, *, agent: Agent, tool_use: ToolUse, **kwargs: Any
    ) -> ToolSteeringAction:
        name = tool_use["name"]
        args = tool_use.get("input", {}) or {}

        if name == "delete_user":
            # Destructive — pause for human approval via the interrupt system.
            return Interrupt(reason=f"Approve deleting user {args.get('user_id')!r}?")

        if name == "send_email" and args.get("to", "").endswith("@example.com"):
            # Not destructive, but wrong audience — guide the model to retry.
            return Guide(reason="example.com is a test domain. Use a real recipient.")

        return Proceed(reason="ok")


agent = Agent(
    tools=[delete_user, send_email],
    plugins=[PolicyHandler()],
)


if __name__ == "__main__":
    # Guided: model will retry with a different recipient.
    agent("Email status@example.com to confirm the build passed.")

    # Interrupted: caller must approve before delete_user runs.
    # See 08_interrupts/tool_interrupt.py for the resume pattern.
    result = agent("Delete user u-42.")
    if result.stop_reason == "interrupt":
        print("Awaiting approval:", [i.data for i in result.interrupts])
