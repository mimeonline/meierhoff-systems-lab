import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


WORKSHOP_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Config:
    api_token: str
    model: str
    base_url: str


def load_config() -> Config:
    load_dotenv(WORKSHOP_ROOT / ".env")

    return Config(
        api_token=os.getenv("LLM_API_TOKEN", ""),
        model=os.getenv("LLM_API_MODEL", "openai/gpt-4.1-mini"),
        base_url=os.getenv("LLM_API_MODELS_BASE_URL", "https://models.github.ai/inference"),
    )
