"""Access performance metrics from agent responses."""

from strands import Agent, tool


@tool
def calculate(expr: str):
    """Evaluate a math expression."""
    return str(eval(expr))


agent = Agent(tools=[calculate])
result = agent("What is 100 * 50 + 25?")

metrics = result.metrics

# Token usage
usage = metrics.accumulated_usage
print(f"Tokens: {usage.get('inputTokens', 0)} in, {usage.get('outputTokens', 0)} out")

# Latency
print(f"Latency: {metrics.accumulated_metrics.get('latencyMs', 0)}ms")

# Cycles (reasoning iterations)
print(f"Cycles: {metrics.cycle_count}")

# Tool stats
for name, tool_metrics in metrics.tool_metrics.items():
    print(f"Tool '{name}': {tool_metrics.call_count} calls, {tool_metrics.success_rate*100:.0f}% success")

# Full summary as dict
# print(metrics.get_summary())
