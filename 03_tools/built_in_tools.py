"""Built-in Tools - Using strands-tools package."""
# pip install strands-agents-tools
from strands import Agent
from strands_tools import calculator, current_time, python_repl

# Create agent with built-in tools
agent = Agent(
    tools=[calculator, current_time, python_repl],
    system_prompt="You have access to calculator, time, and Python tools."
)

# Agent uses appropriate tools
agent("What is the square root of 1691?")
agent("What time is it?")
agent("Write Python code to generate first 10 Fibonacci numbers")
