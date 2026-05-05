import re

from langgraph.graph import END, START, StateGraph

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def orchestrator(state: AgentState) -> AgentState:
    selected_specialist = "math_agent" if _looks_like_math(state["input"]) else "text_agent"
    delegation_brief = _build_delegation_brief(selected_specialist, state["input"])
    note = f"orchestrator delegated to {selected_specialist}"
    return {
        "route": selected_specialist,
        "delegation_brief": delegation_brief,
        "messages": state.get("messages", []) + [note],
        "trace": state.get("trace", [])
        + [
            {
                "actor": "orchestrator",
                "action": "created delegation brief",
                "content": delegation_brief,
            }
        ],
    }


def math_agent(state: AgentState) -> AgentState:
    answer = ask_llm(
        "You are the math specialist. Only handle the delegated math responsibility.",
        f"Delegation brief:\n{state['delegation_brief']}\n\nOriginal request:\n{state['input']}",
    )
    return {
        "specialist_result": answer,
        "messages": state.get("messages", []) + ["math_agent completed delegated work"],
        "trace": state.get("trace", [])
        + [
            {
                "actor": "math_agent",
                "action": "completed delegated specialist work",
                "content": answer,
            }
        ],
    }


def text_agent(state: AgentState) -> AgentState:
    answer = ask_llm(
        "You are the text specialist. Only handle the delegated writing responsibility.",
        f"Delegation brief:\n{state['delegation_brief']}\n\nOriginal request:\n{state['input']}",
    )
    return {
        "specialist_result": answer,
        "messages": state.get("messages", []) + ["text_agent completed delegated work"],
        "trace": state.get("trace", [])
        + [
            {
                "actor": "text_agent",
                "action": "completed delegated specialist work",
                "content": answer,
            }
        ],
    }


def orchestrator_review(state: AgentState) -> AgentState:
    final = (
        f"Selected specialist: {state['route']}\n\n"
        f"Delegation brief:\n{state['delegation_brief']}\n\n"
        f"Specialist output:\n{state['specialist_result']}"
    )
    return {
        "result": final,
        "messages": state.get("messages", []) + ["orchestrator reviewed specialist output"],
        "trace": state.get("trace", [])
        + [
            {
                "actor": "orchestrator",
                "action": "reviewed specialist output",
                "content": f"Accepted output from {state['route']} and assembled final response.",
            }
        ],
    }


def selected_agent(state: AgentState) -> str:
    return state["route"]


def _looks_like_math(text: str) -> bool:
    lowered = text.lower()
    if re.search(r"\d+\s*[-+*/%]\s*\d+", lowered):
        return True
    return any(word in lowered for word in ["calculate", "sum", "multiply", "divide", "percent"])


def _build_delegation_brief(specialist: str, user_input: str) -> str:
    if specialist == "math_agent":
        responsibility = "Solve numeric or quantitative parts. Keep assumptions explicit."
        output = "Return the calculation and the final numeric answer."
    else:
        responsibility = "Improve wording, structure, and clarity. Avoid doing unrelated analysis."
        output = "Return a clearer formulation and a short rationale."

    return "\n".join(
        [
            f"Role: {specialist}",
            f"Request: {user_input}",
            f"Responsibility: {responsibility}",
            f"Expected output: {output}",
        ]
    )


builder = StateGraph(AgentState)
builder.add_node("orchestrator", orchestrator)
builder.add_node("math_agent", math_agent)
builder.add_node("text_agent", text_agent)
builder.add_node("orchestrator_review", orchestrator_review)
builder.add_edge(START, "orchestrator")
builder.add_conditional_edges(
    "orchestrator",
    selected_agent,
    {"math_agent": "math_agent", "text_agent": "text_agent"},
)
builder.add_edge("math_agent", "orchestrator_review")
builder.add_edge("text_agent", "orchestrator_review")
builder.add_edge("orchestrator_review", END)
graph = builder.compile()


def run_graph(user_input: str) -> str:
    state = run_graph_with_trace(user_input)
    return state["result"]


def run_graph_with_trace(user_input: str) -> AgentState:
    return graph.invoke({"input": user_input, "messages": [], "trace": []})
