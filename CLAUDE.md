# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

This is a **cookbook of standalone examples** for the [Strands Agents SDK](https://github.com/strands-agents/sdk-python). Each file under the numbered directories (`01_getting_started/` … `14_safety/`) is self-contained and runnable on its own — there is no shared application code to wire together. The unnumbered directories at the repo root (`basic_agent/`, `agent_with_model/`, `state/`, `agent_vs_api/`, `bedrock_model/`, `built_in_tools/`, `callback_handler/`, `async_iterator/`, `mcp_tools_stdio/`) are older/legacy versions of the same examples and should generally not be edited unless asked — the numbered `NN_topic/` tree is the canonical layout.

A vendored clone of the SDK source lives at `/Users/bp/projects/cloned_repos/strands-sdk-python/src/strands/` — when you need to verify a class signature, hook event field, or import path, grep there rather than guessing or fetching docs.

## Environment & commands

Python `>=3.13` (per `pyproject.toml`), managed with `uv` (see `uv.lock`).

```bash
# Sync the env (creates .venv)
uv sync

# Run any example
uv run python 01_getting_started/basic_agent.py
uv run python 04_mcp/mcp_stdio.py

# Add a dependency
uv add <package>
```

The repo has no test suite, no linter config, and no build step — examples are the deliverables. There is nothing to "build" or "test"; verification is by running the example.

Most examples require external credentials/services:
- Bedrock examples → AWS credentials in env (`AWS_PROFILE` or `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`), default region `us-west-2`
- `02_models/model_providers.py` → `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` as needed
- Ollama examples → local Ollama running on `http://localhost:11434`
- MCP examples → `uvx` available on PATH (used to launch MCP servers like `awslabs.aws-documentation-mcp-server`)
- `13_evals/` → `pip install strands-agents-evals` (not in `pyproject.toml`)
- `14_safety/pii_redaction.py` → LLM Guard (extra install)

## Strands SDK concepts these examples demonstrate

The examples are best understood as a progression through the SDK's main abstractions. When adding or modifying an example, match the conventions of its neighbors:

- **`Agent`** (`strands.Agent`) is the central object. Default model is Bedrock; pass `model=` to swap in `OpenAIModel`, `AnthropicModel`, `GeminiModel`, `OllamaModel`, `LiteLLMModel`, or `BedrockModel` from `strands.models.*`. Models are interchangeable — example code should make swapping providers easy.
- **Tools** are plain Python functions decorated with `@tool` (or `@tool(context=True)` to receive a `ToolContext`). The function's docstring and type hints become the tool schema the LLM sees, so they must be accurate and concise.
- **`ToolContext`** exposes `agent.state` (key-value store, `.get()`/`.set()`), `agent.messages`, `agent.model`, and `interrupt()` for human-in-the-loop. Tools that need any of these declare `context=True`.
- **MCP** (`strands.tools.mcp.MCPClient`) wraps an MCP server. **Everything that uses MCP tools must be inside the `with mcp_client:` block** — outside the context manager the connection is closed and tool calls fail. This is a frequent source of bugs; `04_mcp/mcp_stdio.py` calls it out explicitly. Multiple clients can be combined with `prefix=` and `tool_filters={"allowed"|"rejected": [...]}` to control names and avoid collisions.
- **Sessions** (`strands.session.file_session_manager.FileSessionManager`) persist conversation history to disk between runs; pass via `session_manager=`.
- **Conversation managers** (`strands.agent.conversation_manager.SlidingWindowConversationManager`) bound history length; default window is 20.
- **Hooks** (`strands.hooks`) intercept lifecycle events. The full single-agent set is `AgentInitializedEvent`, `BeforeInvocationEvent`, `MessageAddedEvent`, `BeforeModelCallEvent`, `AfterModelCallEvent`, `BeforeToolCallEvent`, `AfterToolCallEvent`, `AfterInvocationEvent`. Multi-agent orchestrators additionally emit `MultiAgentInitializedEvent`, `Before/AfterNodeCallEvent`, `Before/AfterMultiAgentInvocationEvent`. Three styles, all valid:
  - List of plain callables: `Agent(hooks=[on_before_tool, ...])` — event type is **inferred from the first parameter's type annotation**. Lambdas and untyped callbacks won't work; the type hint is required.
  - `HookProvider` subclass implementing `register_hooks(registry)` — used for stateful hooks like the Bedrock guardrails shadow-mode hook in `14_safety/guardrails_with_hooks.py`.
  - `Plugin` subclass (`strands.plugins`) with `@hook`-decorated methods — auto-discovered, can also expose `@tool` methods; pass via `plugins=[...]` (not `hooks=`).
  - Do **not** pass `hooks={Event: cb, ...}` as a dict — that form is not supported in current SDK versions.
- **Multi-agent** patterns live in `09_multi_agent/`: `GraphBuilder` (`strands.multiagent`) for fixed pipelines via `add_node`/`add_edge`; `Swarm` for dynamic handoffs; `Agent.as_tool()` to expose one agent as a tool of another; `A2AServer` / `strands.agent.a2a_agent.A2AAgent` for cross-process agents over the A2A protocol (`strands-agents[a2a]` extra).
- **Steering** (`strands.vended_plugins.steering`) subclasses `Plugin` and intercepts tool/model events, returning `Proceed` / `Guide` (cancel + feed reason back to the model) / `Interrupt` (escalate to human). Use for graduated safety beyond hard guardrails.
- **Tool executors** (`strands.tools.executors`) — pass `tool_executor=SequentialToolExecutor()` to force serial tool calls; default is `ConcurrentToolExecutor`.
- **ToolProvider** (`strands.tools.tool_provider.ToolProvider`) — implement `load_tools` + `add_consumer` / `remove_consumer` to ship a managed tool bundle (MCP clients are the canonical example). Pass instances directly to `tools=[...]`.
- **Interrupts** — a tool calls `tool_context.interrupt(data)` to pause; the caller sees `result.stop_reason == "interrupt"` and resumes via `agent(interruptResponse={"interrupt_id": ..., "response": ...})`.
- **Streaming** — pass `callback_handler=fn` to receive `data` chunks (`05_streaming/callback_handler.py`); or call `agent.stream_async()` for an async iterator (`05_streaming/async_iterator.py`). Pass `callback_handler=None` to silence the default streaming print.
- **Observability** — `strands.telemetry.StrandsTelemetry` configures OpenTelemetry; `trace_attributes={...}` on the `Agent` propagates onto all spans. Requires `pip install 'strands-agents[otel]'`.

## House style for example code

These conventions are followed across the cookbook — match them when editing or adding examples:

- One concept per file. Triple-quoted module docstring at the top stating what the example shows and any extra `pip install` it needs.
- Real, runnable code at module scope when possible; gate longer demos behind `if __name__ == "__main__":`.
- Keep examples minimal — no error handling, retries, or production scaffolding unless the example is specifically about that.
- Comments explain *why*, not *what*. Inline comments are short and only where the API has a non-obvious gotcha (e.g. the MCP context-manager warning).
- When showing multiple variations of one API (e.g. all the ways to configure `Agent`), declare each variant as a separate top-level binding rather than nesting them — see `01_getting_started/agent_with_model.py`.
- `README.md` is the table of contents; keep it in sync when adding a new example file.
