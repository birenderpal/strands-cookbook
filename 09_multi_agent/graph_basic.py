"""Graph pattern - agents in a pipeline."""

from strands import Agent
from strands.multiagent import GraphBuilder

researcher = Agent(
    name="researcher",
    system_prompt="Research topics and provide facts. Be concise."
)

writer = Agent(
    name="writer", 
    system_prompt="Write content based on research. Keep it brief."
)

reviewer = Agent(
    name="reviewer",
    system_prompt="Review and improve the writing. Output final version."
)

# Build pipeline: researcher -> writer -> reviewer
builder = GraphBuilder()
builder.add_node(researcher, "research")
builder.add_node(writer, "write")
builder.add_node(reviewer, "review")
builder.add_edge("research", "write")
builder.add_edge("write", "review")

graph = builder.build()

if __name__ == "__main__":
    result = graph("Write a paragraph about renewable energy")
    print(result)
