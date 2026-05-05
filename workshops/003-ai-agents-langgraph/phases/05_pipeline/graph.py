from langgraph.graph import END, START, StateGraph

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def analyze(state: AgentState) -> AgentState:
    analysis = ask_llm(
        "You analyze user requests for a workshop pipeline. Identify intent in one sentence.",
        state["input"],
    )
    return {"analysis": analysis, "messages": state.get("messages", []) + [f"analysis: {analysis}"]}


def process(state: AgentState) -> AgentState:
    draft = ask_llm(
        "You process a request after analysis. Produce the useful core answer.",
        f"Analysis:\n{state['analysis']}\n\nRequest:\n{state['input']}",
    )
    return {"result": draft, "messages": state.get("messages", []) + ["process: draft created"]}


def respond(state: AgentState) -> AgentState:
    final = ask_llm(
        "You polish a pipeline draft. Keep the response direct and workshop-friendly.",
        f"Original request:\n{state['input']}\n\nDraft:\n{state['result']}",
    )
    return {"result": final, "messages": state.get("messages", []) + ["respond: final response created"]}


builder = StateGraph(AgentState)
builder.add_node("analyze", analyze)
builder.add_node("process", process)
builder.add_node("respond", respond)
builder.add_edge(START, "analyze")
builder.add_edge("analyze", "process")
builder.add_edge("process", "respond")
builder.add_edge("respond", END)
graph = builder.compile()


def run_graph(user_input: str) -> str:
    state = graph.invoke({"input": user_input, "messages": []})
    return state["result"]
