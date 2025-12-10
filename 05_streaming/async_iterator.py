"""Async Iterator Streaming - Using stream_async() for real-time output."""
from strands import Agent, tool
import asyncio

@tool
def get_weather(city: str):
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 72°F"

agent = Agent(tools=[get_weather], callback_handler=None)

async def stream_response():
    async for event in agent.stream_async("What's the weather in Seattle?"):
        if "data" in event:
            # Text chunks as they're generated
            print(event["data"], end="", flush=True)
        elif "current_tool_use" in event:
            tool = event["current_tool_use"]
            if tool.get("name"):
                print(f"\n[Using tool: {tool['name']}]")

asyncio.run(stream_response())
