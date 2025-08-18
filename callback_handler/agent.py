from strands import Agent, tool
from strands.models import BedrockModel
import logging
import random

logger = logging.getLogger("callback_logging")

@tool
def get_order_status(order_id:str):
    """Get the status of an order"""
    statuses = ["in transit", "delivered", "processing", "shipped", "cancelled", "pending"]
    return f"Order {order_id} is {random.choice(statuses)}"

tool_use_ids = []
def callback_handler(**kwargs):
    if "data" in kwargs:
        # Log the streamed data chunks
        logger.info(kwargs["data"], end="")
    elif "current_tool_use" in kwargs:
        tool = kwargs["current_tool_use"]
        if tool["toolUseId"] not in tool_use_ids:
            # Log the tool use
            logger.info(f"\n[Using tool: {tool.get('name')}]")
            tool_use_ids.append(tool["toolUseId"])



# Create a BedrockModel
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-west-2",
    temperature=0.3,
)

# Create an agent with tools 
agent = Agent(
    tools=[get_order_status],
    model=bedrock_model,
    callback_handler=callback_handler
    )

# Ask the agent a question that uses the available tools
message = """
What is the status of my order 2345
"""

result = agent(message)

# Print only the last response
print(result.message)