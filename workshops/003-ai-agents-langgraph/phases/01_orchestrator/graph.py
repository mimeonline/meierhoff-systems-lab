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
        "trace": state.get("trace", [])
        + [
            {
                "actor": "assistant",
                "action": "direct response",
                "content": answer,
            }
        ],
        "result": answer,
    }


builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile()


def run_graph(user_input: str) -> str:
    state = run_graph_with_trace(user_input)
    return state["result"]


def run_graph_with_trace(user_input: str) -> AgentState:
    return graph.invoke({"input": user_input, "messages": [], "trace": []})
