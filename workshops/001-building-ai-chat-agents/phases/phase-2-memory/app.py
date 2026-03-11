"""Phase 2: Chat with Memory.

# NEW IN THIS PHASE:
#   - history list initialized in on_chat_start
#   - history included in model call
#   - history updated after each response

Compared to Phase 1, the model now sees all previous messages.
Follow-up questions work because earlier turns are replayed.
"""

import chainlit as cl
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from helpers import build_model

SYSTEM_PROMPT = "You are a helpful workshop assistant. Answer clearly and concisely."


@cl.on_chat_start
async def on_chat_start():
    # NEW: initialize conversation history
    cl.user_session.set("history", [])
    await cl.Message(
        content="Phase 2: chat with memory. I can see our conversation history."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    model = build_model()
    response = await model.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        *history,                                  # NEW: replay earlier turns
        HumanMessage(content=message.content),
    ])
    # NEW: store both sides of the turn for next time
    updated = [*history, HumanMessage(content=message.content), AIMessage(content=response.content)]
    cl.user_session.set("history", updated)
    await cl.Message(content=response.content).send()
