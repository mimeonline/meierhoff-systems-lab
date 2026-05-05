import re

from langgraph.graph import END, START, StateGraph

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def analyze(state: AgentState) -> AgentState:
    route = "math" if _looks_like_math(state["input"]) else "text"
    scratchpad = state.get("scratchpad", []) + [
        f"analyze: request classified as {route}",
        "analyze: downstream node should use the shared scratchpad",
    ]
    return {"route": route, "analysis": f"Route selected: {route}", "scratchpad": scratchpad}


def math_agent(state: AgentState) -> AgentState:
    context = "\n".join(state.get("scratchpad", []))
    answer = ask_llm(
        "You are a math specialist. Use the shared context and provide a compact answer.",
        f"Shared context:\n{context}\n\nRequest:\n{state['input']}",
    )
    scratchpad = state.get("scratchpad", []) + ["math_agent: produced numeric answer draft"]
    return {"scratchpad": scratchpad, "result": answer}


def text_agent(state: AgentState) -> AgentState:
    context = "\n".join(state.get("scratchpad", []))
    answer = ask_llm(
        "You are a text specialist. Use the shared context and provide a compact answer.",
        f"Shared context:\n{context}\n\nRequest:\n{state['input']}",
    )
    scratchpad = state.get("scratchpad", []) + ["text_agent: produced explanation draft"]
    return {"scratchpad": scratchpad, "result": answer}


def reviewer(state: AgentState) -> AgentState:
    notes = "\n".join(f"- {item}" for item in state.get("scratchpad", []))
    final = f"{state['result']}\n\nBlackboard notes:\n{notes}"
    return {"result": final, "messages": state.get("messages", []) + ["reviewer: finalized from shared state"]}


def choose_route(state: AgentState) -> str:
    return state["route"]


def _looks_like_math(text: str) -> bool:
    lowered = text.lower()
    if re.search(r"\d+\s*[-+*/%]\s*\d+", lowered):
        return True
    return any(word in lowered for word in ["calculate", "sum", "multiply", "divide", "percent"])


builder = StateGraph(AgentState)
builder.add_node("analyze", analyze)
builder.add_node("math_agent", math_agent)
builder.add_node("text_agent", text_agent)
builder.add_node("reviewer", reviewer)
builder.add_edge(START, "analyze")
builder.add_conditional_edges("analyze", choose_route, {"math": "math_agent", "text": "text_agent"})
builder.add_edge("math_agent", "reviewer")
builder.add_edge("text_agent", "reviewer")
builder.add_edge("reviewer", END)
graph = builder.compile()


def run_graph(user_input: str) -> str:
    state = graph.invoke({"input": user_input, "messages": [], "scratchpad": []})
    return state["result"]
