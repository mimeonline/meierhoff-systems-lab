# Phase 1: Plain Chat

Baseline Chainlit chat backed by a GitHub Models LLM.

## What's New

- Minimal chat interface with one model call per message
- This is the reference point – no memory, no tools

## What To Observe

- Each turn is handled independently
- Follow-up questions lose context
- The model answers only from its built-in knowledge

## Try In Chat

```
My name is Alex.
What is my name?
```

The second answer will not reliably remember the first message.
