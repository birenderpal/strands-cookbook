from strands import Agent
from strands_tools import calculator, current_time, retrieve
from strands.models import BedrockModel
import os
import random

# Create an agent with tools from the strands-tools example tools package
os.environ['KNOWLEDGE_BASE_ID']="8AEEIVKR5U"
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-west-2",
    temperature=0.3,
)

SYSTEM_PROMT="""
You are a helpful assistant who has access to tools. You would only answer questions which can be answered using the tools you have access to. 
If none of the tool can provide the answer do not answer the question using your own knowledge. 
"""
agent = Agent(
    tools=[calculator,current_time,retrieve],
    model=bedrock_model,
    system_prompt=SYSTEM_PROMT
    )
# Ask the agent a question that uses the available tools
messages = [
    # "What is square root of 1691?",
    # "What is the date 2 days from today?"
    # "What is the time in Australia right now?"
    "What is S3 Vector bucket"
]
for message in messages:
    agent(message)
