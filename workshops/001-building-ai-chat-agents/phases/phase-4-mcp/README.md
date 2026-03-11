# Phase 4: Chat with MCP Tool

Same knowledge search, but reached through MCP instead of a direct function call.

## What's New

- `mcp_server.py` exposes the search as an MCP tool
- `app.py` loads MCP tools via `langchain-mcp-adapters` instead of defining them locally
- The MCP server starts automatically over stdio – no manual startup needed

## What To Observe

- The answers are similar to Phase 3 – the capability is the same
- The tool is now discovered and called through a protocol boundary
- Capability and transport are separate architectural concerns

## Try In Chat

```
What is MCP?
What are AI agents?
```

Compare the behavior with Phase 3. The answers are similar, but the architecture is different.
