"""Conversation Managers - Control how conversation history is managed."""
from strands import Agent
from strands.agent.conversation_manager import (
    NullConversationManager,
    SlidingWindowConversationManager,
    SummarizingConversationManager,
)

# 1. Null - No management (history grows forever)
agent_null = Agent(conversation_manager=NullConversationManager())

# 2. Sliding Window - Keep last N messages (default)
agent_sliding = Agent(
    conversation_manager=SlidingWindowConversationManager(
        window_size=20,  # Keep last 20 messages
        should_truncate_results=True  # Truncate large tool results
    )
)

# 3. Summarizing - Summarize old messages instead of dropping
agent_summarizing = Agent(
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.3,  # Summarize 30% when needed
        preserve_recent_messages=10  # Always keep last 10
    )
)

# Test sliding window
for i in range(25):
    agent_sliding(f"Message number {i}")

print(f"Messages kept: {len(agent_sliding.messages)}")
