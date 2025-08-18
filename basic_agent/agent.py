from strands import Agent, tool
from strands_tools import calculator, current_time, python_repl
import random

@tool
def get_order_status(order_id:str):
    """Get the status of an order"""
    statuses = ["in transit", "delivered", "processing", "shipped", "cancelled", "pending"]
    return f"Order {order_id} is {random.choice(statuses)}"

# Create an agent with tools from the strands-tools example tools package
# as well as our custom letter_counter tool
agent = Agent(tools=[get_order_status])

# Ask the agent a question that uses the available tools
message = """
What is the status of my order 2345
"""
agent(message)