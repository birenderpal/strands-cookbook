"""Filter and prefix MCP tools to control what's available."""

import re
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient


# Only load specific tools by name
filtered = MCPClient(
    lambda: stdio_client(StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )),
    tool_filters={"allowed": ["search_documentation", "read_documentation"]}
)


# Filter by regex
regex_filtered = MCPClient(
    lambda: stdio_client(StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )),
    tool_filters={"allowed": [re.compile(r"^search_.*")]}
)


# Exclude specific tools
excluded = MCPClient(
    lambda: stdio_client(StdioServerParameters(
        command="uvx",
        args=["some-mcp-server"]
    )),
    tool_filters={"rejected": ["dangerous_tool", "admin_tool"]}
)


# Add prefix to avoid name collisions when using multiple servers
prefixed = MCPClient(
    lambda: stdio_client(StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )),
    prefix="aws"  # tools become aws_search_documentation, etc.
)


if __name__ == "__main__":
    with filtered:
        tools = filtered.list_tools_sync()
        print(f"Filtered tools: {[t.tool_name for t in tools]}")
