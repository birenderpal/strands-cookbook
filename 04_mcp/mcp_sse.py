"""MCP over Server-Sent Events - for HTTP servers using SSE transport."""

from mcp.client.sse import sse_client
from strands import Agent
from strands.tools.mcp import MCPClient


sse_client_instance = MCPClient(
    lambda: sse_client("http://localhost:8000/sse"),
    startup_timeout=60  # wait up to 60s for server
)


if __name__ == "__main__":
    # Start your MCP server first, e.g.:
    # uvx some-mcp-server --transport sse --port 8000
    
    with sse_client_instance:
        tools = sse_client_instance.list_tools_sync()
        print(f"Found {len(tools)} tools")
        
        agent = Agent(tools=tools)
        response = agent("What tools do you have?")
        print(response)
