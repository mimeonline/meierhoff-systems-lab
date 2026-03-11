from __future__ import annotations

"""Phase 4 compares two paths to the same capability.

The workshop assistant can search the same local knowledge in two ways:
- directly through a local Python tool
- indirectly through an MCP server plus LangChain MCP adapter

This file is intentionally the orchestration layer. It owns:
- the direct tool exposed to the agent
- the MCP server startup configuration
- MCP discovery and adapter loading
- the LangChain agent setup

The actual knowledge-search capability stays in `tools.py`.
"""

from contextlib import asynccontextmanager
import logging
import os
import sys
from pathlib import Path
from typing import Any
from typing import AsyncIterator

import chainlit as cl
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tools import MCP_TOOL_NAME, search_knowledge

load_dotenv()

logger = logging.getLogger(__name__)
MCP_SERVER_PATH = Path(__file__).resolve().parent / "mcp_server.py"
SYSTEM_PROMPT = """You are a concise workshop assistant.

You have two different ways to search the same workshop knowledge:
- `search_knowledge_direct`: direct in-process Python function call
- `search_knowledge_mcp`: the same capability reached through an MCP server and adapter

When the user explicitly asks for "direct", "local", or "without MCP", use `search_knowledge_direct`.
When the user explicitly asks for "MCP", "through MCP", or "via adapter", use `search_knowledge_mcp`.
When the user asks to compare the two, use both tools and explain the architectural difference clearly.

Keep final answers short, clear, and technical.
"""


def build_server_parameters() -> StdioServerParameters:
    """Describe how the local MCP server should be started."""

    logger.info("phase4 mcp build_server_parameters server_path=%s", MCP_SERVER_PATH)
    return StdioServerParameters(command=sys.executable, args=[str(MCP_SERVER_PATH)])


@asynccontextmanager
async def mcp_session() -> AsyncIterator[ClientSession]:
    """Start the local MCP server over stdio and yield an initialized session."""

    logger.info("phase4 mcp_session starting_stdio_server")
    async with stdio_client(build_server_parameters()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            logger.info("phase4 mcp_session initializing_client")
            await session.initialize()
            logger.info("phase4 mcp_session initialized")
            yield session
    logger.info("phase4 mcp_session closed")


async def discover_mcp_tool() -> tuple[str, str]:
    """Start the MCP server, query its tools, and return the knowledge tool."""

    logger.info("phase4 discover_mcp_tool start")
    async with mcp_session() as session:
        listed = await session.list_tools()
        logger.info(
            "phase4 discover_mcp_tool listed_tools=%s",
            [getattr(tool, "name", "") for tool in getattr(listed, "tools", [])],
        )
        for tool in getattr(listed, "tools", []):
            if getattr(tool, "name", "") == MCP_TOOL_NAME:
                logger.info("phase4 discover_mcp_tool found=%s", tool.name)
                return tool.name, getattr(tool, "description", "MCP tool ready.")

    logger.error("phase4 discover_mcp_tool missing=%s", MCP_TOOL_NAME)
    raise ValueError(f"Could not discover MCP tool `{MCP_TOOL_NAME}`.")


@tool("search_knowledge_direct")
async def search_knowledge_direct_tool(query: str) -> str:
    """Search workshop knowledge through a direct local Python function call."""

    logger.info("phase4 tool_call name=search_knowledge_direct query=%r", query)
    async with cl.Step(name="search_knowledge_direct", type="tool", show_input="json") as step:
        step.input = {"query": query}
        result = search_knowledge(query)
        step.output = result
        logger.info("phase4 tool_result name=search_knowledge_direct chars=%s", len(result))
        return result


def build_model() -> ChatOpenAI:
    """Create the chat model client from environment configuration."""

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GITHUB_TOKEN.")

    logger.info("phase4 build_model model=%s", os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"))
    return ChatOpenAI(
        model=os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"),
        api_key=token,
        base_url=os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference"),
        temperature=0,
    )


async def run_agent(user_input: str, history: list[Any]) -> list[Any]:
    """Run a LangChain agent that can choose between direct and MCP tool paths."""

    logger.info("phase4 agent_start user_input=%r history_len=%s", user_input, len(history))
    async with mcp_session() as session:
        # The adapter converts discovered MCP tools into LangChain tools that
        # can be passed directly to a LangChain agent.
        mcp_tools = await load_mcp_tools(session)
        logger.info("phase4 loaded_mcp_tools names=%s", [tool.name for tool in mcp_tools])
        visible_tools = [search_knowledge_direct_tool, *[wrap_tool_with_chainlit_step(tool) for tool in mcp_tools]]
        agent = create_agent(
            model=build_model(),
            tools=visible_tools,
            system_prompt=SYSTEM_PROMPT,
        )
        result = await agent.ainvoke({"messages": [*history, {"role": "user", "content": user_input}]})
        logger.info("phase4 agent_done message_count=%s", len(result["messages"]))
        return result["messages"]


def wrap_tool_with_chainlit_step(tool: BaseTool) -> BaseTool:
    """Wrap an MCP-loaded LangChain tool so its calls are visible in Chainlit."""

    async def wrapped_tool(**kwargs: Any) -> str:
        logger.info("phase4 tool_call name=%s args=%s", tool.name, kwargs)
        async with cl.Step(name=tool.name, type="tool", show_input="json") as step:
            step.input = kwargs
            result = await tool.ainvoke(kwargs)
            step.output = result
            logger.info("phase4 tool_result name=%s chars=%s", tool.name, len(str(result)))
            return result

    return StructuredTool.from_function(
        coroutine=wrapped_tool,
        name=tool.name,
        description=tool.description,
        args_schema=tool.args_schema,
    )


@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialize history and explain the two available tool paths."""

    cl.user_session.set("history", [])
    # Discovery makes the MCP boundary visible at startup.
    tool_name, description = await discover_mcp_tool()
    logger.info("phase4 chat_start discovered_tool=%s", tool_name)
    await cl.Message(
        content=(
            "Phase 4: compare direct tool calls with MCP-backed tool calls. "
            f"Discovered MCP tool `{tool_name}`. {description} "
            "Try asking for `direct`, `MCP`, or `compare both` to make the difference visible."
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle one user turn by running the comparison-focused agent."""

    history = cl.user_session.get("history") or []

    try:
        logger.info("phase4 user_message content=%r history_len=%s", message.content, len(history))
        updated_history = await run_agent(message.content, history)
        cl.user_session.set("history", updated_history)
        final_message = updated_history[-1]
        logger.info("phase4 final_message_type=%s", type(final_message).__name__)
        await cl.Message(content=getattr(final_message, "content", str(final_message))).send()
    except Exception as exc:  # pragma: no cover - workshop runtime guard
        logger.exception("phase4 runtime_error")
        await cl.Message(content=f"Configuration or runtime error: {exc}").send()
