from __future__ import annotations

"""Phase 3 introduces tool use.

The application still keeps conversation history, but the model can now decide
whether to call a local tool before writing the final answer. This is the first
phase where the chat starts to feel agent-like.
"""

import logging
import os
from typing import Any

import chainlit as cl
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from tools import search_knowledge

load_dotenv()

logger = logging.getLogger(__name__)
SYSTEM_PROMPT = """You are a concise workshop assistant.

Use the search_knowledge tool when the user asks about AI agents, tools, or MCP and local notes would help.
Keep final answers short, clear, and technical.
"""


@tool("search_knowledge")
async def search_knowledge_tool(query: str) -> str:
    """Search the local workshop knowledge notes for concise reference material."""

    logger.info("phase3 tool_call name=search_knowledge query=%r", query)
    async with cl.Step(name="search_knowledge", type="tool", show_input="json") as step:
        step.input = {"query": query}
        result = search_knowledge(query)
        step.output = result
        logger.info("phase3 tool_result name=search_knowledge chars=%s", len(result))
        return result


def build_model() -> ChatOpenAI:
    """Create the chat model client from environment configuration."""

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GITHUB_TOKEN.")

    logger.info("phase3 build_model model=%s", os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"))
    return ChatOpenAI(
        model=os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"),
        api_key=token,
        base_url=os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference"),
        temperature=0,
    )


async def run_agent(user_input: str, history: list[Any]) -> list[Any]:
    """Run a LangChain agent with one local tool.

    LangChain now owns the reasoning loop and decides when to call the tool.
    We only pass in the model, tools, system prompt, and prior messages.
    """

    logger.info("phase3 agent_start user_input=%r history_len=%s", user_input, len(history))
    agent = create_agent(
        model=build_model(),
        tools=[search_knowledge_tool],
        system_prompt=SYSTEM_PROMPT,
    )
    result = await agent.ainvoke({"messages": [*history, {"role": "user", "content": user_input}]})
    logger.info("phase3 agent_done message_count=%s", len(result["messages"]))
    return result["messages"]


@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialize empty history and explain the new capability."""

    cl.user_session.set("history", [])
    logger.info("phase3 chat_start history_initialized")
    await cl.Message(
        content="Phase 3: chat with a local knowledge tool. Ask about AI agents, tools, or MCP."
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle one user turn by running the agent and saving history."""

    history = cl.user_session.get("history") or []

    try:
        logger.info("phase3 user_message content=%r history_len=%s", message.content, len(history))
        updated_history = await run_agent(message.content, history)
        cl.user_session.set("history", updated_history)
        final_message = updated_history[-1]
        logger.info("phase3 final_message_type=%s", type(final_message).__name__)
        await cl.Message(content=getattr(final_message, "content", str(final_message))).send()
    except Exception as exc:  # pragma: no cover - workshop runtime guard
        logger.exception("phase3 runtime_error")
        await cl.Message(content=f"Configuration or runtime error: {exc}").send()
