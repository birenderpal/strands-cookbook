from strands import Agent, tool
import random

@tool
def get_order_status(order_id:str):
    """Get the status of an order"""
    statuses = ["in transit", "delivered", "processing", "shipped", "cancelled", "pending"]
    return f"Order {order_id} is {random.choice(statuses)}"

@tool
def get_user_details(agent:Agent):
    """Get the user details"""
    name = agent.state.get("name") or "No Name"
    

    return f"User Name: {name}"

state={"name": "Birender"}
# Create an agent with tool
agent = Agent(tools=[get_order_status,get_user_details],state=state)

# Ask the agent a question that uses the available tools
message = """
What is the status of my order 2345 and what is my name?
"""
agent(message)