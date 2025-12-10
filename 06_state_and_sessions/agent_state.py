"""Agent State - Key-value storage outside conversation context."""
from strands import Agent, tool, ToolContext

@tool(context=True)
def track_action(action: str, tool_context: ToolContext):
    """Track a user action in agent state."""
    count = tool_context.agent.state.get("action_count") or 0
    tool_context.agent.state.set("action_count", count + 1)
    tool_context.agent.state.set("last_action", action)
    return f"Tracked: {action} (total: {count + 1})"

@tool(context=True)
def get_stats(tool_context: ToolContext):
    """Get action statistics."""
    count = tool_context.agent.state.get("action_count") or 0
    last = tool_context.agent.state.get("last_action") or "none"
    return f"Actions: {count}, Last: {last}"

# Initialize with state
agent = Agent(
    tools=[track_action, get_stats],
    state={"user_name": "Alice", "action_count": 0}
)

agent("Track that I logged in")
agent("Track that I viewed dashboard")
agent("What are my stats?")

# Access state directly
print(f"Final state: {agent.state.get()}")
