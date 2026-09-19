"""Agent-as-tool — wrap an Agent so another agent can call it like a function.

This is the third canonical multi-agent pattern alongside Graph (fixed pipeline)
and Swarm (dynamic handoff). Use it when an orchestrator needs to delegate a
self-contained subtask without ceding control of the conversation.

The wrapped agent receives a single `input` string parameter and returns its
text response. Pass agent instances directly to `tools=[...]` to auto-wrap with
defaults, or call `.as_tool()` to customize name/description/context behavior.
"""

from strands import Agent


researcher = Agent(
    name="researcher",
    description="Researches a topic and returns key facts. Use for any factual lookup.",
    system_prompt="Return 3-5 bullet points of factual information. Be concise.",
)

translator = Agent(
    name="translator",
    description="Translates English text into the requested target language.",
    system_prompt="Translate the input. Reply with only the translation.",
)


# Orchestrator picks which sub-agent to call based on the task.
# By default `.as_tool()` resets the sub-agent's conversation between calls
# so each invocation is independent. Pass preserve_context=True to keep history.
orchestrator = Agent(
    system_prompt="Use researcher to gather facts, then translator to localize them.",
    tools=[
        researcher.as_tool(),
        translator.as_tool(preserve_context=True),
    ],
)


if __name__ == "__main__":
    orchestrator("Research the Great Barrier Reef and give me the result in Spanish.")
