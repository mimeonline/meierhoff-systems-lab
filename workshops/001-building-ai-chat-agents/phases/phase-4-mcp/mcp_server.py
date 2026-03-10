from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from tools import MCP_TOOL_NAME
from tools import search_knowledge

server = FastMCP("workshop-knowledge")


@server.tool(name=MCP_TOOL_NAME)
def search_knowledge_mcp(query: str) -> str:
    """Search the workshop knowledge base through MCP."""

    return search_knowledge(query)


if __name__ == "__main__":
    server.run(transport="stdio")
