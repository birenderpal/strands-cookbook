"""FastAPI server exposing a Strands agent as an HTTP endpoint.

Container-friendly deployment target (Fargate, ECS, EKS, Cloud Run, etc.).
Each request gets its own Agent instance bound to a session_id; conversation
state lives in the session manager (file/S3/custom), not in process memory,
so the service is safe to scale horizontally.

  pip install fastapi uvicorn
  uvicorn 12_deployment.fastapi_server:app --reload

Production checklist:
  - put a real auth layer in front (this example has none)
  - replace FileSessionManager with S3SessionManager for multi-replica setups
  - configure model timeouts / retry strategy on the Agent
  - export OTEL traces (see 11_observability/traces_console.py)
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from strands import Agent
from strands.session.file_session_manager import FileSessionManager


SYSTEM_PROMPT = "You are a helpful assistant."
SESSIONS_DIR = os.environ.get("STRANDS_SESSIONS_DIR", "./sessions")


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    yield


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    session_id: str
    prompt: str


@app.post("/chat")
def chat(req: ChatRequest) -> dict:
    agent = Agent(
        system_prompt=SYSTEM_PROMPT,
        session_manager=FileSessionManager(session_id=req.session_id, storage_dir=SESSIONS_DIR),
        callback_handler=None,
    )
    result = agent(req.prompt)
    return {"response": str(result), "session_id": req.session_id}


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}
