"""MCP Elicitation - server can pause and ask user for confirmation.

This is useful for dangerous operations like deleting files.
"""

from mcp import stdio_client, StdioServerParameters
from mcp.types import ElicitResult
from strands import Agent
from strands.tools.mcp import MCPClient


async def handle_elicitation(context, params):
    """Called when MCP server needs user input."""
    print(f"\nServer asks: {params.message}")
    
    # In a real app, show a dialog. Here we just prompt.
    approved = input("Approve? (y/n): ").lower() == "y"
    
    if approved:
        return ElicitResult(action="accept", content={"confirmed": True})
    return ElicitResult(action="reject", content={})


# Create client with elicitation handler
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(command="python", args=["my_mcp_server.py"])
    ),
    elicitation_callback=handle_elicitation
)


# Example MCP server that uses elicitation (save as my_mcp_server.py):
#
# from mcp.server import FastMCP
# from pydantic import BaseModel
#
# class Confirmation(BaseModel):
#     confirmed: bool
#
# server = FastMCP("my-server")
#
# @server.tool()
# async def delete_file(path: str) -> str:
#     result = await server.get_context().elicit(
#         message=f"Delete {path}?",
#         schema=Confirmation,
#     )
#     if result.action != "accept":
#         return "Cancelled"
#     return f"Deleted {path}"
#
# server.run()


if __name__ == "__main__":
    print("This example needs an MCP server with elicitation.")
    print("See the server code in comments above.")
    
    # with mcp_client:
    #     agent = Agent(tools=mcp_client.list_tools_sync())
    #     agent("Delete config.txt")
