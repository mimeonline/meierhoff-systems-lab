# Phase 2: Chat with Memory

Same chat app, but now with conversation history.

## What's New

- History list initialized in `on_chat_start`
- Previous messages replayed to the model on every turn
- History updated after each response

## What To Observe

- Follow-up questions work reliably
- The model can refer to things said earlier
- Memory improves continuity but does not add new capabilities

## Try In Chat

```
My name is Alex.
What is my name?
```

The second answer now works because the app sends prior messages back to the model.
