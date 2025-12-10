"""Interrupts let tools pause for human approval."""

from strands import Agent, tool, ToolContext


@tool(context=True)
def delete_file(filename: str, tool_context: ToolContext):
    """Delete a file (requires approval)."""
    # Pause and return control to the caller
    tool_context.interrupt({"action": "delete", "file": filename})
    
    # Only reaches here after resume
    return f"Deleted {filename}"


agent = Agent(tools=[delete_file])


if __name__ == "__main__":
    result = agent("Delete config.txt")
    
    if result.stop_reason == "interrupt":
        print("Agent paused for approval")
        for interrupt in result.interrupts:
            print(f"  Pending: {interrupt.data}")
        
        # In a real app, you'd show a UI and get user input
        approved = input("Approve? (y/n): ").lower() == "y"
        
        if approved:
            result = agent(
                interruptResponse={
                    "interrupt_id": result.interrupts[0].id,
                    "response": {"approved": True}
                }
            )
            print(f"Result: {result.message}")
        else:
            print("Cancelled")
    else:
        print(f"Result: {result.message}")
