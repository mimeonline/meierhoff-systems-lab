from uuid import uuid4

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from phases.lib.llm import ask_llm
from phases.lib.types import AgentState


def assess(state: AgentState) -> AgentState:
    confidence = _estimate_confidence(state["input"])
    needs_human = confidence < 0.65
    human_question = _build_human_question(state["input"], confidence) if needs_human else ""
    gate_note = (
        "Stop before respond. A human must clarify the assumption below."
        if needs_human
        else "Continue directly to respond."
    )
    return {
        "confidence": confidence,
        "needs_human": needs_human,
        "human_question": human_question,
        "messages": state.get("messages", []) + [f"confidence: {confidence:.2f}"],
        "trace": state.get("trace", [])
        + [
            {
                "actor": "assess",
                "action": "checked confidence and control point",
                "content": (
                    f"Confidence: {confidence:.2f}\n"
                    f"Human review needed: {needs_human}\n"
                    f"Intervention point: {gate_note}\n"
                    f"Human question: {human_question or 'none'}"
                ),
            }
        ],
    }


def human_review(state: AgentState) -> AgentState:
    if not state.get("needs_human", False):
        return {
            "human_feedback": "No human review needed.",
            "trace": state.get("trace", [])
            + [
                {
                    "actor": "human_review",
                    "action": "skipped review",
                    "content": "Confidence was high enough to continue without interruption.",
                }
            ],
        }

    feedback = interrupt(
        {
            "reason": "Confidence is low.",
            "intervention_point": "before respond",
            "question": state["human_question"],
            "input": state["input"],
            "confidence": state.get("confidence", 0.0),
        }
    )
    feedback_text = str(feedback)
    return {
        "human_feedback": feedback_text,
        "trace": state.get("trace", [])
        + [
            {
                "actor": "human_review",
                "action": "paused before respond and resumed",
                "content": (
                    f"Intervention point: before respond\n"
                    f"Question to human: {state['human_question']}\n"
                    f"Human feedback: {feedback_text}"
                ),
            }
        ],
    }


def respond(state: AgentState) -> AgentState:
    feedback = state.get("human_feedback", "No human review needed.")
    question = state.get("human_question", "")
    answer = ask_llm(
        "You are a workshop assistant. Use human feedback when present and answer clearly.",
        (
            f"Request:\n{state['input']}\n\n"
            f"Confidence: {state.get('confidence', 1.0):.2f}\n"
            f"Human control question:\n{question or 'No human question.'}\n"
            f"Human feedback:\n{feedback}"
        ),
    )
    prefix = (
        "Human intervention point: before respond\n"
        f"Question: {question}\n"
        f"Simulated human feedback: {feedback}"
        if state.get("needs_human")
        else "High confidence path."
    )
    result = f"{prefix}\n\n{answer}"
    return {
        "result": result,
        "trace": state.get("trace", [])
        + [
            {
                "actor": "respond",
                "action": "answered after control point",
                "content": result,
            }
        ],
    }


def route_after_assessment(state: AgentState) -> str:
    return "human_review" if state.get("needs_human", False) else "respond"


def _estimate_confidence(text: str) -> float:
    lowered = text.lower()
    uncertainty_markers = ["maybe", "unclear", "not sure", "ambiguous", "risky", "kritisch", "unsicher"]
    if "?" in text and any(marker in lowered for marker in uncertainty_markers):
        return 0.35
    if any(marker in lowered for marker in uncertainty_markers):
        return 0.45
    if len(text.split()) < 4:
        return 0.5
    return 0.82


def _build_human_question(text: str, confidence: float) -> str:
    return (
        "Before the assistant answers, which assumption should be made explicit "
        f"for this low-confidence request ({confidence:.2f})?\nRequest: {text}"
    )


builder = StateGraph(AgentState)
builder.add_node("assess", assess)
builder.add_node("human_review", human_review)
builder.add_node("respond", respond)
builder.add_edge(START, "assess")
builder.add_conditional_edges("assess", route_after_assessment, {"human_review": "human_review", "respond": "respond"})
builder.add_edge("human_review", "respond")
builder.add_edge("respond", END)
graph = builder.compile(checkpointer=MemorySaver())


def run_graph(user_input: str) -> str:
    state = run_graph_with_trace(user_input)
    return state["result"]


def run_graph_with_trace(user_input: str) -> AgentState:
    config = {"configurable": {"thread_id": str(uuid4())}}
    initial_state = {"input": user_input, "messages": [], "trace": []}
    first = graph.invoke(initial_state, config=config)

    if "__interrupt__" not in first:
        return first

    feedback = (
        "Simulated human feedback: answer with a clear assumption, state uncertainty, "
        "and keep the recommendation reversible."
    )
    return graph.invoke(Command(resume=feedback), config=config)
