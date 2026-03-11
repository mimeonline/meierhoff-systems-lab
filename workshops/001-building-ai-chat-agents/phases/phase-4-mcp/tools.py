from __future__ import annotations

"""Shared knowledge-search capability for phase 4.

This file intentionally contains only the reusable search logic and constants.
It does not start the MCP server and does not manage MCP sessions.

That separation is deliberate for the workshop:
- `tools.py` = capability
- `app.py` = orchestration and transport
- `mcp_server.py` = MCP exposure layer
"""

import re
from pathlib import Path

MCP_TOOL_NAME = "search_knowledge_mcp"
KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"


def search_knowledge(query: str) -> str:
    """Search local Markdown notes for a concise workshop-friendly result.

    The same function is used by:
    - the direct tool path in `app.py`
    - the MCP server in `mcp_server.py`
    """

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
    """Return one short matching line so tool outputs stay easy to inspect."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        lowered = line.lower()
        if any(term in lowered for term in terms):
            return line

    return lines[0] if lines else "No content available."
