"""Agent with Custom Tools - Using the @tool decorator."""
from strands import Agent, tool
import random

@tool
def get_order_status(order_id: str):
    """Get the status of an order.
    
    Args:
        order_id: The order ID to check
    """
    statuses = ["in transit", "delivered", "processing", "shipped"]
    return f"Order {order_id} is {random.choice(statuses)}"

@tool
def letter_counter(letter: str, text: str):
    """Count occurrences of a letter in text.
    
    Args:
        letter: The letter to count
        text: The text to search
    """
    return f"'{letter}' appears {text.lower().count(letter.lower())} times"

# Create agent with custom tools
agent = Agent(tools=[get_order_status, letter_counter])

# Agent will use tools as needed
agent("What is the status of order ABC123?")
agent("How many times does 'e' appear in 'Hello World'?")
