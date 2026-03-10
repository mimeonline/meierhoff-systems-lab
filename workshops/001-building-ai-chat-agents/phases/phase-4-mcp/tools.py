from __future__ import annotations

import re
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MCP_SERVER_PATH = Path(__file__).resolve().parent / "mcp_server.py"
MCP_TOOL_NAME = "search_knowledge_mcp"
KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"


def build_server_parameters() -> StdioServerParameters:
    return StdioServerParameters(command=sys.executable, args=[str(MCP_SERVER_PATH)])


def search_knowledge(query: str) -> str:
    """Search local Markdown notes for a concise workshop-friendly result."""

    query = query.strip()
    if not query:
        return "Please provide a query."

    terms = [term for term in re.findall(r"[a-zA-Z0-9-]+", query.lower()) if len(term) > 1]
    matches: list[tuple[int, Path, str]] = []

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        score = sum(lowered.count(term) for term in terms)
        if score:
            matches.append((score, path, excerpt_from(text, terms)))

    if not matches:
        available = ", ".join(path.stem for path in sorted(KNOWLEDGE_DIR.glob("*.md")))
        return f"No strong match found. Available notes: {available}."

    matches.sort(key=lambda item: (-item[0], item[1].name))
    top = matches[:2]
    return "\n\n".join(f"{path.stem} (score: {score})\n{excerpt}" for score, path, excerpt in top)


def excerpt_from(text: str, terms: list[str]) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        lowered = line.lower()
        if any(term in lowered for term in terms):
            return line

    return lines[0] if lines else "No content available."


async def discover_mcp_tool() -> tuple[str, str]:
    """Connect to the local MCP server and discover the knowledge tool."""

    async with stdio_client(build_server_parameters()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            listed = await session.list_tools()
            for tool in getattr(listed, "tools", []):
                if getattr(tool, "name", "") == MCP_TOOL_NAME:
                    return tool.name, getattr(tool, "description", "MCP tool ready.")

    raise ValueError(f"Could not discover MCP tool `{MCP_TOOL_NAME}`.")


async def call_mcp_tool(query: str) -> str:
    """Call the discovered MCP tool and return its text content."""

    async with stdio_client(build_server_parameters()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(MCP_TOOL_NAME, {"query": query})
            content = []
            for item in getattr(result, "content", []) or []:
                text = getattr(item, "text", None)
                if text:
                    content.append(text)
            return "\n".join(content) if content else "The MCP tool returned no text."
