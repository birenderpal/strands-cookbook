from strands import Agent, tool
from strands_tools import calculator, current_time, python_repl
from strands.models import BedrockModel

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
agent = Agent(tools=[get_order_status],model=bedrock_model)

# Ask the agent a question that uses the available tools
message = """
What is the status of my order 2345
"""
agent(message)