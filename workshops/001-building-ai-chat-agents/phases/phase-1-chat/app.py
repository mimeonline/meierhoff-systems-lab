"""Phase 1: Plain Chat – no memory, no tools.

Every user turn is handled in isolation.
The model receives only one system instruction and the current message.
"""

import chainlit as cl
from langchain_core.messages import HumanMessage, SystemMessage

from helpers import build_model

SYSTEM_PROMPT = "You are a helpful workshop assistant. Answer clearly and concisely."


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Phase 1: plain chat. I only see your current message."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    model = build_model()
    response = await model.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        # Only the current user turn – no history.
        HumanMessage(content=message.content),
    ])
    await cl.Message(content=response.content).send()
