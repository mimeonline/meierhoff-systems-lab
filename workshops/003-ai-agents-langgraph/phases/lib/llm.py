import ast
import operator
import re
from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from phases.lib.config import Config, load_config


@dataclass
class ChatResult:
    content: str


class WorkshopLLM:
    """Small ChatOpenAI-compatible adapter for GitHub Models or OpenAI-style APIs."""

    def __init__(self, config: Config):
        self.config = config
        self.client = None
        if config.api_token:
            self.client = OpenAI(api_key=config.api_token, base_url=config.base_url)

    def invoke(self, messages: list[dict[str, str]], temperature: float = 0.2) -> ChatResult:
        if self.client is None:
            return ChatResult(_offline_response(messages))

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=temperature,
        )
        content = response.choices[0].message.content or ""
        return ChatResult(content.strip())


def get_llm() -> WorkshopLLM:
    return WorkshopLLM(load_config())


def ask_llm(system: str, user: str, temperature: float = 0.2) -> str:
    llm = get_llm()
    return llm.invoke(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    ).content


def _offline_response(messages: list[dict[str, str]]) -> str:
    user = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
    maybe_result = _safe_arithmetic(user)
    if maybe_result is not None:
        return f"Local fallback answer: the arithmetic result is {maybe_result}."

    return (
        "Local fallback answer: no LLM_API_TOKEN is configured. "
        f"I would handle this request as a concise assistant response: {user}"
    )


def _safe_arithmetic(text: str) -> str | None:
    match = re.search(r"[-+*/(). 0-9]{3,}", text)
    if not match:
        return None

    expression = match.group(0).strip()
    if not re.search(r"\d\s*[-+*/]\s*\d", expression):
        return None

    try:
        value = _eval_ast(ast.parse(expression, mode="eval").body)
    except Exception:
        return None

    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value)


def _eval_ast(node: ast.AST) -> Any:
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in operators:
        return operators[type(node.op)](_eval_ast(node.left), _eval_ast(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
        return operators[type(node.op)](_eval_ast(node.operand))
    raise ValueError("Unsupported arithmetic expression")
