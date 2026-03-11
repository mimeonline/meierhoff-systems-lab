"""Phase 5: Compare Direct Tool vs MCP Tool.

# NEW IN THIS PHASE:
#   - Both a direct local tool AND an MCP tool are available
#   - The model can choose which path to use
#   - Same capability, different architecture

This phase makes the architectural difference between direct and MCP visible.
"""

import chainlit as cl
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_mcp_adapters.tools import load_mcp_tools

from helpers import build_model, mcp_session, wrap_tool_with_chainlit_step
from tools import search_knowledge

SYSTEM_PROMPT = """You are a helpful workshop assistant with two ways to search the same knowledge:

- `search_knowledge_direct`: calls the Python function directly in this process
- `search_knowledge_mcp`: calls the same function through an MCP server

When the user says "direct" or "local", use search_knowledge_direct.
When the user says "MCP", use search_knowledge_mcp.
When the user says "compare", use both and explain the architectural difference.
Keep answers short and clear.
"""


# From Phase 3: a direct local tool
@tool("search_knowledge_direct")
async def search_knowledge_direct_tool(query: str) -> str:
    """Search workshop knowledge through a direct local function call."""
    async with cl.Step(name="search_knowledge_direct", type="tool") as step:
        step.input = {"query": query}
        result = search_knowledge(query)
        step.output = result
        return result


# NEW: both direct and MCP tools offered to the same agent
async def run_agent(user_input: str, history: list) -> list:
    async with mcp_session() as session:
        mcp_tools = await load_mcp_tools(session)
        tools = [
            search_knowledge_direct_tool,
            *[wrap_tool_with_chainlit_step(t) for t in mcp_tools],
        ]
        agent = create_agent(
            model=build_model(),
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
        )
        result = await agent.ainvoke(
            {"messages": [*history, {"role": "user", "content": user_input}]}
        )
        return result["messages"]


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Phase 5: compare direct vs MCP tool calls. Try 'direct', 'MCP', or 'compare both'."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    messages = await run_agent(message.content, history)
    cl.user_session.set("history", messages)
    await cl.Message(content=getattr(messages[-1], "content", str(messages[-1]))).send()
