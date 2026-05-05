from typing import TypedDict


class TraceEvent(TypedDict):
    actor: str
    action: str
    content: str


class AgentState(TypedDict, total=False):
    input: str
    messages: list[str]
    trace: list[TraceEvent]
    route: str
    analysis: str
    delegation_brief: str
    specialist_result: str
    blackboard: dict[str, str]
    scratchpad: list[str]
    result: str
    confidence: float
    needs_human: bool
    human_feedback: str
