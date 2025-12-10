"""Using ToolContext to access agent internals from within tools.

ToolContext gives you access to:
- agent.state: key-value storage
- agent.messages: conversation history  
- agent.model: the model being used
- interrupt(): pause for human input
"""

from strands import Agent, tool, ToolContext
from datetime import datetime


# Track searches and maintain history
@tool(context=True)
def log_search(query: str, tool_context: ToolContext):
    """Log a search query and track search history."""
    history = tool_context.agent.state.get("search_history") or []
    history.append({"query": query, "time": datetime.now().isoformat()})
    tool_context.agent.state.set("search_history", history)
    tool_context.agent.state.set("total_searches", len(history))
    
    return f"Found 42 results for '{query}'"


# Store user preferences
@tool(context=True)
def set_preference(name: str, value: str, tool_context: ToolContext):
    """Store a user preference."""
    prefs = tool_context.agent.state.get("preferences") or {}
    prefs[name] = value
    tool_context.agent.state.set("preferences", prefs)
    return f"Set {name} = {value}"


@tool(context=True)
def get_preference(name: str, tool_context: ToolContext):
    """Get a stored preference."""
    prefs = tool_context.agent.state.get("preferences") or {}
    value = prefs.get(name)
    return f"{name} = {value}" if value else f"No preference '{name}' found"


# Check conversation length
@tool(context=True)
def conversation_stats(tool_context: ToolContext):
    """Get stats about the current conversation."""
    messages = tool_context.agent.messages
    user_msgs = sum(1 for m in messages if m.get("role") == "user")
    return f"Conversation has {user_msgs} user messages"


# Simple rate limiting
@tool(context=True)
def expensive_api_call(data: str, tool_context: ToolContext):
    """An operation with usage limits."""
    usage = tool_context.agent.state.get("api_calls") or 0
    limit = tool_context.agent.state.get("api_limit") or 10
    
    if usage >= limit:
        return f"Rate limit exceeded ({usage}/{limit})"
    
    tool_context.agent.state.set("api_calls", usage + 1)
    return f"Processed '{data}' ({usage + 1}/{limit} calls used)"


if __name__ == "__main__":
    agent = Agent(
        tools=[log_search, set_preference, get_preference, 
               conversation_stats, expensive_api_call],
        state={"api_limit": 3}
    )
    
    agent("Set my language preference to Spanish")
    agent("What is my language preference?")
    agent("Search for 'python tutorials'")
    agent("Search for 'machine learning'")
    
    print(f"\nFinal state: {agent.state.get()}")
