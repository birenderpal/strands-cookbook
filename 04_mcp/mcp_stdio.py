"""MCP stdio Transport - Connect to local MCP servers."""
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

# Create MCP client with stdio transport
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )
))

# IMPORTANT: Everything must be inside the context manager
with mcp_client:
    tools = mcp_client.list_tools_sync()
    print(f"Loaded {len(tools)} tools from MCP server")
    
    agent = Agent(tools=tools)
    response = agent("What is AWS Lambda?")
    print(response)

# Outside the 'with' block, MCP connection is closed
# Agent cannot use MCP tools here!
