"""
Bedrock Guardrails - native integration with Strands.

Requires: Create a guardrail in AWS Bedrock console first.
"""
import json
from strands import Agent
from strands.models import BedrockModel

# Bedrock model with guardrails enabled
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    guardrail_id="your-guardrail-id",
    guardrail_version="1",
    guardrail_trace="enabled",  # for debugging
    # Optional: customize redaction behavior
    # guardrail_redact_input=True,  # default: True
    # guardrail_redact_input_message="Input blocked by guardrail",
    # guardrail_redact_output=False,  # default: False
)

agent = Agent(model=model, system_prompt="You are a helpful assistant.")

response = agent("Tell me about financial planning.")

if response.stop_reason == "guardrail_intervened":
    print("Content blocked by guardrails")
    print(f"Messages: {json.dumps(agent.messages, indent=2)}")
else:
    print(response)
