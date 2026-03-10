from __future__ import annotations

import os

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

SYSTEM_PROMPT = "You are a concise workshop assistant. Keep answers clear and technical."


def build_model() -> ChatOpenAI:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GITHUB_TOKEN.")

    return ChatOpenAI(
        model=os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"),
        api_key=token,
        base_url=os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference"),
        temperature=0,
    )


@cl.on_chat_start
async def on_chat_start() -> None:
    await cl.Message(
        content="Phase 1: plain chat. I only see your current message."
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    try:
        model = build_model()
        response = await model.ainvoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=message.content),
            ]
        )
        await cl.Message(content=response.content).send()
    except Exception as exc:  # pragma: no cover - workshop runtime guard
        await cl.Message(content=f"Configuration or runtime error: {exc}").send()
