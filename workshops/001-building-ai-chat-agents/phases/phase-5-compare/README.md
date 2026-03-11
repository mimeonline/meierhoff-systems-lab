# Phase 5: Compare Direct vs MCP

Both a direct local tool and an MCP tool are available in the same agent.

## What's New

- `search_knowledge_direct` calls the Python function directly (like Phase 3)
- `search_knowledge_mcp` calls the same function through an MCP server (like Phase 4)
- The model can choose which path to use based on user instruction

## What To Observe

- The Chainlit UI shows which tool name was used
- The returned knowledge is the same – only the access path differs
- Asking for "compare" makes the architectural difference visible

## Try In Chat

```
Use the direct tool to explain MCP.
Use MCP to explain MCP.
Compare both paths for the same question.
```

Watch the tool names in the Chainlit UI to see which path was taken.
