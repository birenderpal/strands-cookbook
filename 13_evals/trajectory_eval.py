"""Evaluate whether the agent uses the right tools in the right order.

pip install strands-agents-evals
"""

from strands import Agent, tool
from strands_evals import Case, Experiment
from strands_evals.evaluators import TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor


# Tools for an e-commerce agent
@tool
def search_products(query: str, category: str = None):
    """Search the product catalog."""
    return f"Found 5 products for '{query}'"

@tool
def get_product_details(product_id: str):
    """Get product info."""
    return f"Product {product_id}: Widget Pro, $29.99, In Stock"

@tool
def add_to_cart(product_id: str, quantity: int = 1):
    """Add to cart."""
    return f"Added {quantity}x {product_id} to cart"

@tool
def calculate_shipping(zip_code: str):
    """Get shipping cost."""
    return f"Shipping to {zip_code}: $5.99"


def run_agent(case: Case) -> dict:
    """Run agent and capture which tools it used."""
    agent = Agent(
        tools=[search_products, get_product_details, add_to_cart, calculate_shipping],
        callback_handler=None
    )
    result = agent(case.input)
    
    # Extract tool usage sequence
    trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)
    
    return {"output": str(result), "trajectory": trajectory}


# Test cases with expected tool sequences
test_cases = [
    Case[str, str](
        name="search-and-buy",
        input="Find me a laptop and add the first one to my cart",
        expected_trajectory=["search_products", "add_to_cart"],
    ),
    Case[str, str](
        name="product-lookup",
        input="Tell me about product ABC123",
        expected_trajectory=["get_product_details"],
    ),
    Case[str, str](
        name="full-flow",
        input="Search headphones, show details, add to cart, shipping to 90210",
        expected_trajectory=["search_products", "get_product_details", "add_to_cart", "calculate_shipping"],
    ),
]


evaluator = TrajectoryEvaluator(
    rubric="""
    Score based on tool usage:
    - 1.0: All expected tools, logical order
    - 0.5: Some expected tools, reasonable order
    - 0.0: Wrong tools or no tools when needed
    """
)


if __name__ == "__main__":
    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
    reports = experiment.run_evaluations(run_agent)
    
    for case, report in zip(test_cases, reports):
        print(f"\n{case.name}")
        print(f"  Expected: {case.expected_trajectory}")
        if hasattr(report, 'output') and isinstance(report.output, dict):
            print(f"  Actual: {report.output.get('trajectory', [])}")
        report.run_display()
