"""
PII Redaction with LLM Guard - works with any model provider.

pip install llm-guard

Strands doesn't have native PII redaction, so we use third-party libraries.
"""
from strands import Agent
from llm_guard.vault import Vault
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF

vault = Vault()


def create_scanner():
    return Anonymize(vault, recognizer_conf=BERT_LARGE_NER_CONF, language="en")


def redact_pii(text: str) -> str:
    """Redact PII from text before sending to LLM."""
    scanner = create_scanner()
    sanitized, _, _ = scanner.scan(text)
    return sanitized


# Example: sanitize user input before agent processes it
agent = Agent(system_prompt="You are a customer service agent.")

raw_input = "Hi, I'm John Smith. My phone is 555-123-4567 and email is john@example.com"
safe_input = redact_pii(raw_input)
print(f"Sanitized: {safe_input}")
# Output: Hi, I'm [REDACTED_PERSON]. My phone is [REDACTED_PHONE] and email is [REDACTED_EMAIL]

response = agent(safe_input)
print(response)
