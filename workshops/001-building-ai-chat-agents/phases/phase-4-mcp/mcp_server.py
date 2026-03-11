from __future__ import annotations

"""Expose the shared knowledge-search capability through MCP.

This file does not implement the search itself. It only turns the reusable
capability from `tools.py` into an MCP tool that can be discovered and loaded
by the application in `app.py`.
"""

from mcp.server.fastmcp import FastMCP

from tools import MCP_TOOL_NAME
from tools import search_knowledge

server = FastMCP("workshop-knowledge")


@server.tool(name=MCP_TOOL_NAME)
def search_knowledge_mcp(query: str) -> str:
    """Expose the shared knowledge search through an MCP tool."""

    return search_knowledge(query)


if __name__ == "__main__":
    server.run(transport="stdio")
