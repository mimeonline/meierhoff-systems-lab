from langgraph.graph import END, START, StateGraph

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def assistant(state: AgentState) -> AgentState:
    answer = ask_llm(
        "You are a concise workshop assistant. Answer clearly in 3 to 5 sentences.",
        state["input"],
    )
    return {
        "messages": state.get("messages", []) + [f"assistant: {answer}"],
        "result": answer,
    }


builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile()


def run_graph(user_input: str) -> str:
    state = graph.invoke({"input": user_input, "messages": []})
    return state["result"]
