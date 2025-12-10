"""Enable debug logging for the SDK."""

import logging
from strands import Agent, tool

# Set up logging before creating agent
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    level=logging.WARNING
)

# Enable debug for strands
logging.getLogger("strands").setLevel(logging.DEBUG)

# Or be selective:
# logging.getLogger("strands.tools.registry").setLevel(logging.DEBUG)
# logging.getLogger("strands.models").setLevel(logging.WARNING)


@tool
def greet(name: str):
    """Say hello."""
    return f"Hello, {name}!"


agent = Agent(tools=[greet])
response = agent("Say hello to Alice")

# You'll see logs for tool registration, model calls, event loop
