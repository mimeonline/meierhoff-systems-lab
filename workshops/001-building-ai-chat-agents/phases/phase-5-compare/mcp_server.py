"""MCP server that exposes the knowledge search as a tool."""

from mcp.server.fastmcp import FastMCP

from tools import MCP_TOOL_NAME, search_knowledge

server = FastMCP("workshop-knowledge")


@server.tool(name=MCP_TOOL_NAME)
def search_knowledge_mcp(query: str) -> str:
    """Search workshop knowledge notes through MCP."""
    return search_knowledge(query)


if __name__ == "__main__":
    server.run(transport="stdio")
