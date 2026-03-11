from __future__ import annotations

"""Phase 1 shows the smallest possible Chainlit chat application.

The important idea for learners is that every user turn is handled in isolation.
The model receives only:
- one system instruction
- the current user message

There is no memory, no tool use, and no reasoning loop yet.
"""

import logging
import os

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

logger = logging.getLogger(__name__)
SYSTEM_PROMPT = "You are a concise workshop assistant. Keep answers clear and technical."


def build_model() -> ChatOpenAI:
    """Create the chat model client from environment configuration."""

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GITHUB_TOKEN.")

    logger.info("phase1 build_model model=%s", os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"))
    return ChatOpenAI(
        model=os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"),
        api_key=token,
        base_url=os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference"),
        temperature=0,
    )


@cl.on_chat_start
async def on_chat_start() -> None:
    """Send a short explanation when a new chat session begins."""

    logger.info("phase1 chat_start")
    await cl.Message(
        content="Phase 1: plain chat. I only see your current message."
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle one user message with a single model call.

    The key learning point is the message list below: it contains only the
    system prompt and the current user message. Earlier turns are not included.
    """

    try:
        logger.info("phase1 user_message content=%r", message.content)
        model = build_model()
        logger.info("phase1 invoking_model")
        response = await model.ainvoke(
            [
                # The system message sets behavior for the assistant.
                SystemMessage(content=SYSTEM_PROMPT),
                # Only the current user turn is passed to the model.
                HumanMessage(content=message.content),
            ]
        )
        logger.info("phase1 response_chars=%s", len(str(response.content)))
        await cl.Message(content=response.content).send()
    except Exception as exc:  # pragma: no cover - workshop runtime guard
        logger.exception("phase1 runtime_error")
        await cl.Message(content=f"Configuration or runtime error: {exc}").send()
