# Strands Cookbook

Code examples for the Strands Agents SDK. Each file is standalone and runnable.

## Setup

```bash
pip install strands-agents strands-agents-tools
```

## Examples

**Getting Started** (`01_getting_started/`)
- `basic_agent.py` - Hello world
- `agent_with_tools.py` - Custom tools
- `agent_with_model.py` - Config options

**Models** (`02_models/`)
- `bedrock_model.py` - Bedrock with AWS credentials
- `model_providers.py` - OpenAI, Anthropic, Gemini, Ollama, LiteLLM (API keys)

**Tools** (`03_tools/`)
- `built_in_tools.py` - Calculator, time, etc
- `tool_context.py` - Accessing agent state from tools

**MCP** (`04_mcp/`)
- `mcp_stdio.py` - Local servers
- `mcp_sse.py` - SSE transport
- `mcp_streamable_http.py` - HTTP transport
- `mcp_filtering.py` - Filter/prefix tools
- `mcp_elicitation.py` - User confirmation flow

**Streaming** (`05_streaming/`)
- `async_iterator.py` - stream_async()
- `callback_handler.py` - Callbacks

**State & Sessions** (`06_state_and_sessions/`)
- `agent_state.py` - Key-value state
- `conversation_managers.py` - History management
- `file_session.py` - Persist to disk

**Hooks** (`07_hooks/`)
- `basic_hooks.py` - Lifecycle events

**Interrupts** (`08_interrupts/`)
- `tool_interrupt.py` - Human-in-the-loop

**Multi-Agent** (`09_multi_agent/`)
- `graph_basic.py` - Pipeline pattern
- `swarm_basic.py` - Dynamic routing

**Structured Output** (`10_structured_output/`)
- `pydantic_output.py` - Typed responses

**Observability** (`11_observability/`)
- `metrics.py` - Token usage, latency
- `traces_console.py` - OpenTelemetry
- `logging_config.py` - Debug logs

**Evals** (`13_evals/`)
- `output_eval.py` - Response quality
- `trajectory_eval.py` - Tool usage

**Safety** (`14_safety/`)
- `bedrock_guardrails.py` - Native Bedrock guardrails
- `guardrails_with_hooks.py` - Shadow mode via Hooks (any provider)
- `pii_redaction.py` - LLM Guard integration

## Requirements

- Python 3.10+
- AWS credentials for Bedrock examples
- API keys for other providers (OpenAI, Anthropic, Gemini, etc.)
- Extra packages for some examples (noted in files)
