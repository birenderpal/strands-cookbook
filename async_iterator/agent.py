from strands import Agent, tool
from strands.models import BedrockModel
import asyncio

import random

@tool
def get_order_status(order_id:str):
    """Get the status of an order"""
    statuses = ["in transit", "delivered", "processing", "shipped", "cancelled", "pending"]
    return f"Order {order_id} is {random.choice(statuses)}"

# Create an agent with tools 

# Create a BedrockModel
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-west-2",
    temperature=0.3,
)
agent = Agent(
    tools=[get_order_status],
    model=bedrock_model,
    callback_handler=None
    )

# Ask the agent a question that uses the available tools
message = """
What is the status of my order 2345
"""

async def process_streaming_response():    

    # Get an async iterator for the agent's response stream
    agent_stream = agent.stream_async(message)

    # Process events as they arrive
    async for event in agent_stream:
        if "data" in event:
            # Print text chunks as they're generated
            print(event["data"], end="", flush=True)
        elif "current_tool_use" in event and event["current_tool_use"].get("name"):
            # Print tool usage information
            print(f"\n[Tool use delta for: {event['current_tool_use']['name']}]")

# Run the agent with the async event processing
asyncio.run(process_streaming_response())