from strands import Agent, tool
from strands_tools import calculator, current_time, python_repl
from strands.models import BedrockModel

import random

@tool
def sum(a:float,b:float):
    """Adds two numbers together"""
    return a + b
@tool
def divide(a:float, b:float):
    """Divides two numbers"""
    return a / b
@tool
def multiply(a:float, b:float):
    """Multiplies two numbers"""
    return a * b

@tool
def subtract(a:float, b:float):
    """Subtracts two numbers"""
    return a - b

# Create an agent with tools 

# Create a BedrockModel
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-west-2",
    temperature=0.3,
)
agent = Agent(tools=[sum,divide,multiply,subtract],model=bedrock_model)

# Ask the agent a question that uses the available tools
message = """
Calculate 200 + 300 X 2
"""
agent(message)