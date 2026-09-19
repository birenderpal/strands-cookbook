"""Consume a remote A2A agent as if it were a local Strands Agent.

A2AAgent is a client wrapper — it discovers the remote agent's card and forwards
prompts over the A2A protocol. It implements the same call interface as Agent,
so it slots into multi-agent patterns (or `tools=[remote_agent.as_tool()]`).

pip install 'strands-agents[a2a]'

Start a2a_server.py in another shell first.
"""

import asyncio
from strands.agent.a2a_agent import A2AAgent


remote = A2AAgent(
    endpoint="http://127.0.0.1:9000",
    # name/description are auto-populated from the remote Agent Card on first call.
)


async def main():
    # Inspect the remote agent before talking to it.
    card = await remote.get_agent_card()
    print(f"Discovered: {card.name} — {card.description}")
    print(f"Skills: {[s.name for s in card.skills]}\n")

    # Synchronous-style call is also available: remote("...")
    result = await remote.invoke_async("What's the weather in Tokyo?")
    print(result.message)


if __name__ == "__main__":
    asyncio.run(main())
