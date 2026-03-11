"""Shared setup – not part of the learning content."""

import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.tools import BaseTool, StructuredTool
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

WORKSHOP_ROOT = Path(__file__).resolve().parents[2]
PHASE_DIR = Path(__file__).resolve().parent

# Load shared workshop settings first, then let a phase-local `.env` override them.
load_dotenv(WORKSHOP_ROOT / ".env")
load_dotenv(PHASE_DIR / ".env", override=True)

MCP_SERVER_PATH = Path(__file__).resolve().parent / "mcp_server.py"


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


@asynccontextmanager
async def mcp_session() -> AsyncIterator[ClientSession]:
    """Start the local MCP server over stdio and yield a ready session."""
    params = StdioServerParameters(command=sys.executable, args=[str(MCP_SERVER_PATH)])
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session


def wrap_tool_with_chainlit_step(tool: BaseTool) -> BaseTool:
    """Make MCP tool calls visible in the Chainlit UI."""

    async def wrapped(**kwargs: Any) -> str:
        async with cl.Step(name=tool.name, type="tool", show_input="json") as step:
            step.input = kwargs
            result = await tool.ainvoke(kwargs)
            step.output = result
            return result

    return StructuredTool.from_function(
        coroutine=wrapped,
        name=tool.name,
        description=tool.description,
        args_schema=tool.args_schema,
    )
