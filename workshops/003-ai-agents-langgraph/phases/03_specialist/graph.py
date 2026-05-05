import re

from langgraph.graph import END, START, StateGraph

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def orchestrator(state: AgentState) -> AgentState:
    route = "math" if _looks_like_math(state["input"]) else "text"
    note = f"orchestrator selected {route}_agent"
    return {"route": route, "messages": state.get("messages", []) + [note]}


def math_agent(state: AgentState) -> AgentState:
    answer = ask_llm(
        "You are the math specialist in a multi-agent workshop. Solve the problem carefully.",
        state["input"],
    )
    return {"result": f"Specialist: math_agent\n\n{answer}"}


def text_agent(state: AgentState) -> AgentState:
    answer = ask_llm(
        "You are the text specialist in a multi-agent workshop. Improve clarity and explain tradeoffs.",
        state["input"],
    )
    return {"result": f"Specialist: text_agent\n\n{answer}"}


def selected_agent(state: AgentState) -> str:
    return state["route"]


def _looks_like_math(text: str) -> bool:
    lowered = text.lower()
    if re.search(r"\d+\s*[-+*/%]\s*\d+", lowered):
        return True
    return any(word in lowered for word in ["calculate", "sum", "multiply", "divide", "percent"])


builder = StateGraph(AgentState)
builder.add_node("orchestrator", orchestrator)
builder.add_node("math_agent", math_agent)
builder.add_node("text_agent", text_agent)
builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", selected_agent, {"math": "math_agent", "text": "text_agent"})
builder.add_edge("math_agent", END)
builder.add_edge("text_agent", END)
graph = builder.compile()


def run_graph(user_input: str) -> str:
    state = graph.invoke({"input": user_input, "messages": []})
    return state["result"]
