"""
Different model providers with Strands.

API key providers: OpenAI, Anthropic, Gemini (pass api_key in client_args)
AWS credentials: Bedrock (uses IAM, not API keys)
Local: Ollama (no auth needed)

pip install 'strands-agents[openai,anthropic,gemini]'
"""

import os
from strands import Agent

# OpenAI
from strands.models.openai import OpenAIModel

openai_model = OpenAIModel(
    client_args={"api_key": os.environ.get("OPENAI_API_KEY")},
    model_id="gpt-4o",
    params={"temperature": 0.7, "max_tokens": 1000},
)

# works with any OpenAI-compatible endpoint
openai_compatible = OpenAIModel(
    client_args={
        "api_key": os.environ.get("CUSTOM_API_KEY", "not-needed"),
        "base_url": "http://localhost:8000/v1",
    },
    model_id="local-model",
)

# Anthropic
from strands.models.anthropic import AnthropicModel

anthropic_model = AnthropicModel(
    client_args={"api_key": os.environ.get("ANTHROPIC_API_KEY")},
    model_id="claude-sonnet-4-20250514",
    max_tokens=1024,
)

# Gemini
from strands.models.gemini import GeminiModel

gemini_model = GeminiModel(
    client_args={"api_key": os.environ.get("GOOGLE_API_KEY")},
    model_id="gemini-2.5-flash",
)


# Ollama for local models
from strands.models.ollama import OllamaModel

ollama_model = OllamaModel(host="http://localhost:11434", model_id="llama3.2")

# LiteLLM gives you one interface to many providers
from strands.models.litellm import LiteLLMModel

litellm_openai = LiteLLMModel(model_id="gpt-4o")
litellm_bedrock = LiteLLMModel(model_id="bedrock/anthropic.claude-sonnet-4-20250514-v1:0")


if __name__ == "__main__":
    # swap in any model - they're all interchangeable
    agent = Agent(model=openai_model)
    print(agent("What's 2+2?"))
