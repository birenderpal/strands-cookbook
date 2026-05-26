"""S3 Session Manager - Persist conversations to S3 instead of local disk.

Same API as FileSessionManager — swap the manager and conversations sync to S3
across processes / hosts / restarts. Useful for serverless deployments where
local disk is ephemeral (Lambda, Fargate) or for multi-replica services.

Requires the bucket to already exist and the caller to have s3:GetObject /
PutObject / ListObjectsV2 / DeleteObject on the prefix.
"""

import os
from strands import Agent
from strands.session.s3_session_manager import S3SessionManager


session_manager = S3SessionManager(
    session_id="user-123",
    bucket=os.environ["STRANDS_SESSION_BUCKET"],
    prefix="cookbook/sessions",           # all keys land under this prefix
    region_name="us-west-2",
    # boto_session=... and boto_client_config=... for non-default credentials
)

agent = Agent(session_manager=session_manager)

agent("My name is Alice and I love Python.")
agent("What's my favorite programming language?")

# Re-run with the same session_id from any process to resume the conversation.
