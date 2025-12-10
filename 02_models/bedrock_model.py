"""Bedrock Model - AWS Bedrock configuration options."""
from strands import Agent
from strands.models import BedrockModel

# Basic Bedrock model
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-west-2",
)

# With inference parameters
model_with_params = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-west-2",
    temperature=0.7,
    max_tokens=2000,
    top_p=0.9,
)

# With guardrails
model_with_guardrails = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-west-2",
    guardrail_id="your-guardrail-id",
    guardrail_version="1",
)

agent = Agent(model=model_with_params)
response = agent("Write a haiku about coding.")
print(response)
