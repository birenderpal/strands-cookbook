"""Simplest possible agent - just create and call it."""

from strands import Agent

agent = Agent()
response = agent("What is 2 + 2?")
print(response)
