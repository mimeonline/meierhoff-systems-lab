"""Phase 4: Chat with MCP Tool.

# NEW IN THIS PHASE:
#   - Knowledge search is reached through an MCP server (mcp_server.py)
#   - MCP tools are loaded via langchain-mcp-adapters
#   - The capability is the same as Phase 3, but accessed through a protocol boundary

The key insight: capability and transport are separate concerns.
The same search works, but it is now discovered and called through MCP.
"""

import chainlit as cl
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools

from helpers import build_model, mcp_session, wrap_tool_with_chainlit_step

SYSTEM_PROMPT = """You are a helpful workshop assistant with access to knowledge notes through MCP.

When the user asks about AI agents, tools, or MCP, use the search tool.
Keep answers short and clear.
"""


# NEW: agent loads tools from MCP server instead of defining them locally
async def run_agent(user_input: str, history: list) -> list:
    async with mcp_session() as session:
        mcp_tools = await load_mcp_tools(session)
        tools = [wrap_tool_with_chainlit_step(t) for t in mcp_tools]
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
        content="Phase 4: knowledge search through MCP. Ask about AI agents, tools, or MCP."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    messages = await run_agent(message.content, history)
    cl.user_session.set("history", messages)
    await cl.Message(content=getattr(messages[-1], "content", str(messages[-1]))).send()
