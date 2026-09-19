"""ToolProvider — bundle a managed collection of tools with lifecycle hooks.

A ToolProvider is what `tools=[mcp_client]` actually is under the hood: an
object the Agent asks for its tool list and notifies on attach/detach. Write
your own when you need to:

  - load tools dynamically (from a DB, config, or remote service)
  - share expensive resources (DB pool, HTTP session) across many tools
  - reference-count cleanup across multiple consuming agents

For static tools, just pass the @tool functions directly to `tools=[...]`.
"""

from collections.abc import Sequence
from typing import Any
from strands import Agent, tool
from strands.tools.tool_provider import ToolProvider
from strands.types.tools import AgentTool


class FeatureFlaggedTools(ToolProvider):
    """Loads a different set of tools depending on which features are enabled."""

    def __init__(self, features: set[str]) -> None:
        self._features = features
        self._consumers: set[Any] = set()

    async def load_tools(self, **kwargs: Any) -> Sequence[AgentTool]:
        tools: list[AgentTool] = []

        if "billing" in self._features:
            @tool
            def get_invoice(invoice_id: str) -> str:
                """Look up an invoice by id."""
                return f"Invoice {invoice_id}: $42.00"
            tools.append(get_invoice)

        if "admin" in self._features:
            @tool
            def reset_password(user_id: str) -> str:
                """Reset a user's password (admin only)."""
                return f"Password for {user_id} reset."
            tools.append(reset_password)

        return tools

    def add_consumer(self, consumer_id: Any, **kwargs: Any) -> None:
        self._consumers.add(consumer_id)

    def remove_consumer(self, consumer_id: Any, **kwargs: Any) -> None:
        # Must be idempotent — agents may call this twice on cleanup.
        self._consumers.discard(consumer_id)
        if not self._consumers:
            # Last consumer left — release any shared resources here.
            pass


if __name__ == "__main__":
    provider = FeatureFlaggedTools(features={"billing"})
    agent = Agent(tools=[provider])
    agent("Look up invoice INV-7.")
