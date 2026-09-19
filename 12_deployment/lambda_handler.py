"""AWS Lambda handler — Strands agent behind an API Gateway / function URL.

Layout for the deployable bundle (zip or container):

  lambda_handler.py            # this file
  requirements.txt             # strands-agents, strands-agents-tools, etc.

Configuration on the Lambda function:
  - Runtime: Python 3.13
  - Timeout: 60s (model calls can take a while)
  - Memory: 1024 MB minimum (boto3 + tokenizers are not tiny)
  - Execution role: bedrock:InvokeModel*, and s3:* on the session bucket
                    if you enable S3 session persistence
  - Env: STRANDS_SESSION_BUCKET (optional)

Why this pattern works:
  - The Agent + tools are built once at module load (warm-start friendly).
  - Each request is stateless from Lambda's POV; conversation persistence
    lives in S3SessionManager keyed on session_id from the request body.
"""

import json
import os
from strands import Agent, tool
from strands.session.s3_session_manager import S3SessionManager


@tool
def get_order_status(order_id: str) -> str:
    """Get the status of an order."""
    return f"Order {order_id} is in transit."


# Built once per container — survives across warm invocations.
SYSTEM_PROMPT = "You are a customer support agent. Be concise."


def _build_agent(session_id: str) -> Agent:
    bucket = os.environ.get("STRANDS_SESSION_BUCKET")
    session_manager = (
        S3SessionManager(session_id=session_id, bucket=bucket) if bucket else None
    )
    return Agent(
        system_prompt=SYSTEM_PROMPT,
        tools=[get_order_status],
        session_manager=session_manager,
        callback_handler=None,  # Lambda has no terminal — disable streaming print
    )


def handler(event: dict, context: object) -> dict:
    body = json.loads(event.get("body") or "{}")
    session_id = body.get("session_id", "anonymous")
    prompt = body["prompt"]

    agent = _build_agent(session_id)
    result = agent(prompt)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": str(result), "session_id": session_id}),
    }
