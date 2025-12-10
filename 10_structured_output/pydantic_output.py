"""Get typed responses using Pydantic models."""

from strands import Agent
from pydantic import BaseModel, Field
from typing import List


class MovieReview(BaseModel):
    title: str
    rating: float = Field(description="1-10 scale")
    pros: List[str]
    cons: List[str]
    summary: str


agent = Agent()

review = agent.structured_output(
    output_model=MovieReview,
    prompt="Review the movie Inception"
)

# review is a MovieReview instance
print(f"{review.title}: {review.rating}/10")
print(f"Pros: {review.pros}")
print(f"Cons: {review.cons}")
print(f"Summary: {review.summary}")
