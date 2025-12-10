"""Evaluate agent responses against expected outputs.

pip install strands-agents-evals
"""

from strands import Agent
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator


def run_agent(case: Case) -> str:
    """Run the agent and return its response."""
    agent = Agent(
        system_prompt="You are a customer support agent for an e-commerce site.",
        callback_handler=None
    )
    return str(agent(case.input))


# Test cases - questions we expect the agent to handle
test_cases = [
    Case[str, str](
        name="refund-policy",
        input="What is your refund policy?",
        expected_output="30 days, full refund, original payment method",
    ),
    Case[str, str](
        name="shipping-time",
        input="How long does shipping take?",
        expected_output="3-5 business days standard, 1-2 express",
    ),
    Case[str, str](
        name="order-tracking",
        input="How do I track my order?",
        expected_output="Use order number on tracking page or check email",
    ),
    Case[str, str](
        name="out-of-scope",
        input="What's the weather like today?",
        expected_output="Politely redirect to e-commerce topics",
    ),
]


# Rubric tells the evaluator how to score
evaluator = OutputEvaluator(
    rubric="""
    Score 0.0-1.0 based on:
    - 1.0: Correct, complete, professional
    - 0.75: Mostly correct, minor gaps
    - 0.5: Partially correct, missing key info
    - 0.25: Vaguely related but unhelpful
    - 0.0: Wrong or harmful
    """,
    include_inputs=True
)


if __name__ == "__main__":
    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
    reports = experiment.run_evaluations(run_agent)
    
    for report in reports:
        report.run_display()
    
    # Quick summary
    scores = []
    for report in reports:
        for eval_result in report.evaluations:
            if hasattr(eval_result, 'score'):
                scores.append(eval_result.score)
    
    if scores:
        print(f"\nAverage: {sum(scores)/len(scores):.2f}")
        print(f"Pass rate (>0.5): {sum(1 for s in scores if s > 0.5)/len(scores)*100:.0f}%")
