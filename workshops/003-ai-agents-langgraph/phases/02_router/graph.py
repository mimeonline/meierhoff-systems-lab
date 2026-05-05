import re

from langgraph.graph import END, START, StateGraph

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def router(state: AgentState) -> AgentState:
    route = "math" if _looks_like_math(state["input"]) else "text"
    return {"route": route, "messages": state.get("messages", []) + [f"route: {route}"]}


def math_agent(state: AgentState) -> AgentState:
    answer = ask_llm(
        "You are a careful math assistant. Show the important step and final result.",
        state["input"],
    )
    return {"result": f"Route: math\n\n{answer}"}


def text_agent(state: AgentState) -> AgentState:
    answer = ask_llm(
        "You are a concise writing assistant. Explain or rewrite the request clearly.",
        state["input"],
    )
    return {"result": f"Route: text\n\n{answer}"}


def choose_route(state: AgentState) -> str:
    return state["route"]


def _looks_like_math(text: str) -> bool:
    lowered = text.lower()
    if re.search(r"\d+\s*[-+*/%]\s*\d+", lowered):
        return True
    return any(word in lowered for word in ["calculate", "sum", "multiply", "divide", "percent"])


builder = StateGraph(AgentState)
builder.add_node("router", router)
builder.add_node("math_agent", math_agent)
builder.add_node("text_agent", text_agent)
builder.add_edge(START, "router")
builder.add_conditional_edges("router", choose_route, {"math": "math_agent", "text": "text_agent"})
builder.add_edge("math_agent", END)
builder.add_edge("text_agent", END)
graph = builder.compile()


def run_graph(user_input: str) -> str:
    state = graph.invoke({"input": user_input, "messages": []})
    return state["result"]
