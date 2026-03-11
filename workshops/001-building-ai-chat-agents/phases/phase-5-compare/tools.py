"""Local knowledge search – intentionally simple for learning."""

from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent / "knowledge"
MCP_TOOL_NAME = "search_knowledge_mcp"


def search_knowledge(query: str) -> str:
    """Search local Markdown notes by keyword matching."""
    if not query.strip():
        return "Please provide a query."

    words = [w for w in query.lower().split() if len(w) > 2]
    results = []

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text()
        if any(word in text.lower() for word in words):
            results.append(f"From {path.stem}:\n{text.strip()}")

    return "\n\n".join(results) if results else "No match found."
