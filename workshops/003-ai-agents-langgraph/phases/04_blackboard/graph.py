import re

from langgraph.graph import END, START, StateGraph

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def analyze(state: AgentState) -> AgentState:
    route = "math" if _looks_like_math(state["input"]) else "text"
    blackboard = dict(state.get("blackboard", {}))
    blackboard.update(
        {
            "request": state["input"],
            "route": route,
            "analysis": f"Request classified as {route}. Specialist must read and update this shared state.",
        }
    )
    return {
        "route": route,
        "analysis": f"Route selected: {route}",
        "blackboard": blackboard,
        "trace": state.get("trace", [])
        + [
            {
                "actor": "analyze",
                "action": "wrote shared blackboard",
                "content": _format_blackboard(blackboard),
            }
        ],
    }


def math_agent(state: AgentState) -> AgentState:
    blackboard = dict(state.get("blackboard", {}))
    answer = ask_llm(
        "You are a math specialist. Read the blackboard and write a compact draft.",
        f"Blackboard:\n{_format_blackboard(blackboard)}\n\nRequest:\n{state['input']}",
    )
    blackboard.update(
        {
            "specialist": "math_agent",
            "draft": answer,
            "draft_note": "Numeric answer draft added by math_agent.",
        }
    )
    return {
        "blackboard": blackboard,
        "specialist_result": answer,
        "trace": state.get("trace", [])
        + [
            {
                "actor": "math_agent",
                "action": "read and updated blackboard",
                "content": _format_blackboard(blackboard),
            }
        ],
    }


def text_agent(state: AgentState) -> AgentState:
    blackboard = dict(state.get("blackboard", {}))
    answer = ask_llm(
        "You are a text specialist. Read the blackboard and write a compact draft.",
        f"Blackboard:\n{_format_blackboard(blackboard)}\n\nRequest:\n{state['input']}",
    )
    blackboard.update(
        {
            "specialist": "text_agent",
            "draft": answer,
            "draft_note": "Explanation draft added by text_agent.",
        }
    )
    return {
        "blackboard": blackboard,
        "specialist_result": answer,
        "trace": state.get("trace", [])
        + [
            {
                "actor": "text_agent",
                "action": "read and updated blackboard",
                "content": _format_blackboard(blackboard),
            }
        ],
    }


def reviewer(state: AgentState) -> AgentState:
    blackboard = dict(state.get("blackboard", {}))
    blackboard["review"] = f"Reviewed {blackboard.get('specialist', 'specialist')} draft from shared state."
    snapshot = _format_blackboard(blackboard)
    final = f"{blackboard.get('draft', '')}\n\nBlackboard snapshot:\n{snapshot}"
    return {
        "result": final,
        "blackboard": blackboard,
        "messages": state.get("messages", []) + ["reviewer: finalized from shared state"],
        "trace": state.get("trace", [])
        + [
            {
                "actor": "reviewer",
                "action": "read blackboard and finalized",
                "content": snapshot,
            }
        ],
    }


def choose_route(state: AgentState) -> str:
    return state["route"]


def _looks_like_math(text: str) -> bool:
    lowered = text.lower()
    if re.search(r"\d+\s*[-+*/%]\s*\d+", lowered):
        return True
    return any(word in lowered for word in ["calculate", "sum", "multiply", "divide", "percent"])


def _format_blackboard(blackboard: dict[str, str]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in blackboard.items())


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
    state = run_graph_with_trace(user_input)
    return state["result"]


def run_graph_with_trace(user_input: str) -> AgentState:
    return graph.invoke({"input": user_input, "messages": [], "blackboard": {}, "trace": []})
