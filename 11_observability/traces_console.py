"""OpenTelemetry tracing - prints spans to console.

pip install 'strands-agents[otel]'
"""

from strands import Agent
from strands.telemetry import StrandsTelemetry

# Enable console output for traces
telemetry = StrandsTelemetry()
telemetry.setup_console_exporter()

# Add custom attributes to all traces
agent = Agent(
    trace_attributes={
        "session.id": "demo-123",
        "user.id": "test@example.com",
    }
)

response = agent("What is the capital of France?")
print(f"\nResponse: {response}")

# Traces show agent span, cycle spans, model invocations, tool calls
