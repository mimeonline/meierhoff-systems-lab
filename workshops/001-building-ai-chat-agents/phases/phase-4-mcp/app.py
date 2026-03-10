from __future__ import annotations

import os
from typing import Any

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from tools import call_mcp_tool, discover_mcp_tool

load_dotenv()

SYSTEM_PROMPT = """You are a concise workshop assistant.

Use the search_knowledge_mcp tool when the user asks about AI agents, tools, or MCP and local notes would help.
Keep final answers short, clear, and technical.
"""


@tool("search_knowledge_mcp")
async def search_knowledge_mcp_tool(query: str) -> str:
    """Search workshop knowledge through the discovered MCP tool."""

    return await call_mcp_tool(query)


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


async def run_agent(user_input: str, history: list[Any]) -> list[Any]:
    model = build_model().bind_tools([search_knowledge_mcp_tool])
    messages: list[Any] = [SystemMessage(content=SYSTEM_PROMPT), *history, HumanMessage(content=user_input)]

    while True:
        response = await model.ainvoke(messages)
        messages.append(response)

        if not isinstance(response, AIMessage) or not response.tool_calls:
            return messages[1:]

        for call in response.tool_calls:
            result = await call_mcp_tool(call.get("args", {}).get("query", ""))
            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))


@cl.on_chat_start
async def on_chat_start() -> None:
    cl.user_session.set("history", [])
    tool_name, description = await discover_mcp_tool()
    await cl.Message(
        content=(
            "Phase 4: chat with MCP. "
            f"Discovered MCP tool `{tool_name}`. {description}"
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    history = cl.user_session.get("history") or []

    try:
        updated_history = await run_agent(message.content, history)
        cl.user_session.set("history", updated_history)
        final_message = updated_history[-1]
        await cl.Message(content=getattr(final_message, "content", str(final_message))).send()
    except Exception as exc:  # pragma: no cover - workshop runtime guard
        await cl.Message(content=f"Configuration or runtime error: {exc}").send()
