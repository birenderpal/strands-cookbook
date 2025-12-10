"""Swarm pattern - agents hand off to each other dynamically."""

from strands import Agent
from strands.multiagent import Swarm

sales = Agent(
    name="sales",
    system_prompt="Handle sales questions. Hand off to support for technical issues."
)

support = Agent(
    name="support",
    system_prompt="Handle technical support. Hand off to billing for payment issues."
)

billing = Agent(
    name="billing",
    system_prompt="Handle billing and payments."
)

swarm = Swarm(agents=[sales, support, billing])

if __name__ == "__main__":
    # Swarm routes to the right agent based on the question
    result = swarm("I can't log into my account")
    print(result)
