"""MCP over HTTP - for remote MCP servers."""

import os
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient


# Basic HTTP connection
http_client = MCPClient(
    lambda: streamablehttp_client("http://localhost:8000/mcp")
)


# With auth headers (e.g., GitHub Copilot)
github_client = MCPClient(
    lambda: streamablehttp_client(
        url="https://api.githubcopilot.com/mcp/",
        headers={"Authorization": f"Bearer {os.getenv('GITHUB_PAT')}"}
    )
)


# AWS IAM auth (pip install mcp-proxy-for-aws)
try:
    from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client
    
    aws_client = MCPClient(
        lambda: aws_iam_streamablehttp_client(
            endpoint="https://your-service.us-east-1.amazonaws.com/mcp",
            aws_region="us-east-1",
            aws_service="bedrock-agentcore"
        )
    )
except ImportError:
    pass  # mcp-proxy-for-aws not installed


if __name__ == "__main__":
    with http_client:
        tools = http_client.list_tools_sync()
        print(f"Found {len(tools)} tools")
        
        agent = Agent(tools=tools)
        response = agent("What can you do?")
        print(response)
