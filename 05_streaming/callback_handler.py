"""Callback Handler Streaming - Using callback_handler for events."""
from strands import Agent, tool

@tool
def calculate(expression: str):
    """Evaluate a math expression."""
    return str(eval(expression))

seen_tools = set()

def my_callback(**kwargs):
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)
    elif "current_tool_use" in kwargs:
        tool = kwargs["current_tool_use"]
        tool_id = tool.get("toolUseId")
        if tool_id and tool_id not in seen_tools:
            print(f"\n[Tool: {tool.get('name')}]")
            seen_tools.add(tool_id)

agent = Agent(tools=[calculate], callback_handler=my_callback)
result = agent("What is 15 * 23?")
print(f"\n\nFinal: {result.message}")
