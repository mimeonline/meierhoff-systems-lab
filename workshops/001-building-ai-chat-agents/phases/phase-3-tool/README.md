# Phase 3: Chat with Tool

The model can now call a local `search_knowledge` tool.

## What's New

- `search_knowledge(query)` tool in `tools.py`
- LangChain agent with reasoning loop replaces direct `model.ainvoke()`
- Model decides when to call the tool

## What To Observe

- Some questions trigger tool use (visible as a step in the Chainlit UI)
- The response flow becomes multi-step: decide, call tool, observe result, answer
- This is where the system starts to feel agent-like

## Try In Chat

```
What is MCP?
Summarize it in one sentence.
```

Watch the Chainlit UI for visible tool steps showing input and output.
