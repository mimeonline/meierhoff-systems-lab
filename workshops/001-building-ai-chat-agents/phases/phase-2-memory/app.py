from __future__ import annotations

"""Phase 2 adds short-term conversation memory.

Compared to phase 1, the application now stores earlier user and assistant
messages in the Chainlit session and sends them back to the model on each turn.
This makes follow-up questions work more naturally.
"""

import logging
import os
from typing import Any

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

logger = logging.getLogger(__name__)
SYSTEM_PROMPT = "You are a concise workshop assistant. Keep answers clear and technical."


def build_model() -> ChatOpenAI:
    """Create the chat model client from environment configuration."""

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GITHUB_TOKEN.")

    logger.info("phase2 build_model model=%s", os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"))
    return ChatOpenAI(
        model=os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"),
        api_key=token,
        base_url=os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference"),
        temperature=0,
    )


@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialize empty conversation history for this browser session."""

    # Chainlit stores session-scoped values per user chat session.
    cl.user_session.set("history", [])
    logger.info("phase2 chat_start history_initialized")
    await cl.Message(
        content="Phase 2: chat with memory. I can see the current conversation history."
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle one user message while preserving prior turns.

    The main learning step is that we read `history`, include it in the model
    input, and then write an updated version back into the session.
    """

    history = cl.user_session.get("history") or []

    try:
        logger.info("phase2 user_message content=%r history_len=%s", message.content, len(history))
        model = build_model()
        messages: list[Any] = [
            SystemMessage(content=SYSTEM_PROMPT),
            # Earlier turns are replayed so the model can continue the dialog.
            *history,
            HumanMessage(content=message.content),
        ]
        logger.info("phase2 invoking_model message_count=%s", len(messages))
        response = await model.ainvoke(messages)
        # We store both sides of the latest turn for the next request.
        updated_history = [*history, HumanMessage(content=message.content), AIMessage(content=response.content)]
        cl.user_session.set("history", updated_history)
        logger.info("phase2 updated_history_len=%s response_chars=%s", len(updated_history), len(str(response.content)))
        await cl.Message(content=response.content).send()
    except Exception as exc:  # pragma: no cover - workshop runtime guard
        logger.exception("phase2 runtime_error")
        await cl.Message(content=f"Configuration or runtime error: {exc}").send()
