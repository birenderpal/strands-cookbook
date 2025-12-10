"""File Session Manager - Persist conversations to filesystem."""
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

# Create session manager
session_manager = FileSessionManager(
    session_id="user-123",
    storage_dir="./sessions"  # Optional, defaults to temp dir
)

# Create agent with session persistence
agent = Agent(session_manager=session_manager)

# First conversation - gets persisted
agent("My name is Alice and I love Python.")
agent("What's my favorite programming language?")

print("Session saved. Restart script to test persistence.")

# To test: Run script twice. Second run will remember the conversation.
