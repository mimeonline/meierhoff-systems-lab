"""Phase 3: Chat with Tool.

# NEW IN THIS PHASE:
#   - search_knowledge tool defined and bound to the agent
#   - LangChain agent with reasoning loop replaces direct model call
#   - Model can decide to call the tool before answering

This is where the system starts to feel agent-like.
The model is no longer limited to prompt and memory.
"""

import chainlit as cl
from langchain.agents import create_agent
from langchain_core.tools import tool

from helpers import build_model
from tools import search_knowledge

SYSTEM_PROMPT = """You are a helpful workshop assistant with access to local knowledge notes.

When the user asks about AI agents, tools, or MCP, search the knowledge notes first.
Then answer based on what you found. Keep answers short and clear.
"""


# NEW: a tool the model can call during the reasoning loop
@tool("search_knowledge")
async def search_knowledge_tool(query: str) -> str:
    """Search the local workshop knowledge notes."""
    async with cl.Step(name="search_knowledge", type="tool") as step:
        step.input = {"query": query}
        result = search_knowledge(query)
        step.output = result
        return result


# NEW: agent with reasoning loop replaces direct model.ainvoke()
async def run_agent(user_input: str, history: list) -> list:
    agent = create_agent(
        model=build_model(),
        tools=[search_knowledge_tool],
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
        content="Phase 3: chat with a local knowledge tool. Ask about AI agents, tools, or MCP."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    messages = await run_agent(message.content, history)
    cl.user_session.set("history", messages)
    await cl.Message(content=getattr(messages[-1], "content", str(messages[-1]))).send()
