from typing import TypedDict


class AgentState(TypedDict, total=False):
    input: str
    messages: list[str]
    route: str
    analysis: str
    scratchpad: list[str]
    result: str
    confidence: float
    needs_human: bool
    human_feedback: str
