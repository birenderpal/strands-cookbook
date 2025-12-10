"""All the ways to configure a Strands agent."""

from strands import Agent
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager


# Minimal - just use defaults
agent_minimal = Agent()


# Pass model as string (uses Bedrock)
agent_model_string = Agent(model="us.amazon.nova-pro-v1:0")


# BedrockModel with inference parameters
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-west-2",
    temperature=0.7,          # 0.0 = deterministic, 1.0 = creative
    max_tokens=2000,
    top_p=0.9,
    stop_sequences=["END"],
)


# System prompt - instructions for the agent
agent_with_prompt = Agent(
    model=bedrock_model,
    system_prompt="""You are a Python expert. Follow these rules:
    1. Always explain code before writing it
    2. Include error handling
    3. Keep responses concise
    """
)


# Conversation manager - override defaults (SlidingWindowConversationManager is used by default)
agent_with_conv_manager = Agent(
    conversation_manager=SlidingWindowConversationManager(
        window_size=40,              # default is 20
        should_truncate_results=False # default is True
    )
)


# Initial state - key-value storage accessible from tools
agent_with_state = Agent(
    state={
        "user_id": "user-123",
        "preferences": {"theme": "dark"},
        "counter": 0
    }
)


# Pre-fill conversation history
agent_with_history = Agent(
    messages=[
        {"role": "user", "content": [{"text": "My name is Alice"}]},
        {"role": "assistant", "content": [{"text": "Nice to meet you, Alice!"}]}
    ]
)


# Custom callback for streaming events
def my_callback(**kwargs):
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)

agent_with_callback = Agent(callback_handler=my_callback)

# Disable default streaming output
agent_silent = Agent(callback_handler=None)


# Trace attributes for observability
agent_with_traces = Agent(
    trace_attributes={
        "session.id": "sess-abc123",
        "user.id": "user@example.com",
        "environment": "production"
    }
)


# Putting it all together
agent_full = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="us-west-2",
        temperature=0.3,
        max_tokens=4000,
    ),
    system_prompt="You are a helpful coding assistant.",
    conversation_manager=SlidingWindowConversationManager(window_size=30),
    state={"session_start": "2024-01-15"},
    trace_attributes={"app": "my-app"},
    callback_handler=my_callback,
)


if __name__ == "__main__":
    response = agent_full("Write a Python function to reverse a string")
    print(f"\n\nDone.")
