"""
Guardrails via Hooks - works with ANY model provider.

How it works:
- Bedrock's ApplyGuardrail API is a standalone endpoint that evaluates text
  against your guardrail policies. It doesn't require Bedrock as your LLM.
- This Hook intercepts messages, sends them to ApplyGuardrail, and logs violations.
- Your agent (OpenAI, Anthropic, Ollama, etc.) processes requests normally.

Shadow mode (notify-only):
- Guardrails evaluate and log but DON'T block requests.
- Useful for testing/tuning guardrails before enforcing them.
- To actually block, raise an exception in the hook instead of printing.

Example flow:
  User input -> Hook calls ApplyGuardrail -> Logs "would block" -> Agent responds anyway
"""
import boto3
from strands import Agent
from strands.hooks import HookProvider, HookRegistry, MessageAddedEvent, AfterInvocationEvent


class GuardrailHook(HookProvider):
    """Evaluates content against Bedrock guardrails without blocking."""

    def __init__(self, guardrail_id: str, guardrail_version: str, region: str = "us-west-2"):
        self.guardrail_id = guardrail_id
        self.guardrail_version = guardrail_version
        self.client = boto3.client("bedrock-runtime", region)

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(MessageAddedEvent, self.check_input)
        registry.add_callback(AfterInvocationEvent, self.check_output)

    def evaluate(self, content: str, source: str = "INPUT"):
        try:
            response = self.client.apply_guardrail(
                guardrailIdentifier=self.guardrail_id,
                guardrailVersion=self.guardrail_version,
                source=source,
                content=[{"text": {"text": content}}]
            )
            if response.get("action") == "GUARDRAIL_INTERVENED":
                print(f"[GUARDRAIL] Would block {source}: {content[:50]}...")
                for a in response.get("assessments", []):
                    if "topicPolicy" in a:
                        for t in a["topicPolicy"].get("topics", []):
                            print(f"  Topic: {t['name']} - {t['action']}")
                    if "contentPolicy" in a:
                        for f in a["contentPolicy"].get("filters", []):
                            print(f"  Content: {f['type']} - {f['confidence']}")
        except Exception as e:
            print(f"[GUARDRAIL] Error: {e}")

    def check_input(self, event: MessageAddedEvent) -> None:
        if event.message.get("role") == "user":
            content = "".join(b.get("text", "") for b in event.message.get("content", []))
            if content:
                self.evaluate(content, "INPUT")

    def check_output(self, event: AfterInvocationEvent) -> None:
        if event.agent.messages and event.agent.messages[-1].get("role") == "assistant":
            msg = event.agent.messages[-1]
            content = "".join(b.get("text", "") for b in msg.get("content", []))
            if content:
                self.evaluate(content, "OUTPUT")


# Works with any model - using default Bedrock here
agent = Agent(
    system_prompt="You are a helpful assistant.",
    hooks=[GuardrailHook("your-guardrail-id", "1")]
)

# Guardrails evaluate but don't block - useful for testing/tuning
response = agent("What's the weather like?")
print(response)
