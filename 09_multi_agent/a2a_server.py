"""Expose a Strands agent over the A2A (Agent-to-Agent) protocol.

Wraps any Strands Agent in an A2AServer that publishes an Agent Card at
`/.well-known/agent-card.json` and accepts A2A messages over HTTP.

pip install 'strands-agents[a2a]'

Run this server, then point a2a_client.py at http://127.0.0.1:9000.
"""

from strands import Agent, tool
from strands.multiagent.a2a import A2AServer


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's sunny and 72F in {city}."


# A2A requires name + description — they populate the Agent Card.
agent = Agent(
    name="weather-agent",
    description="An agent that answers weather questions for any city.",
    system_prompt="You are a weather assistant. Use get_weather for any location.",
    tools=[get_weather],
)

# Skills are auto-derived from the agent's tools when `skills=` is not passed.
server = A2AServer(agent, host="127.0.0.1", port=9000)


if __name__ == "__main__":
    # Blocks. Defaults to Starlette; pass app_type="fastapi" for FastAPI.
    server.serve()
