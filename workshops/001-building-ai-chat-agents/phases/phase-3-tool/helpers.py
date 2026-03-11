"""Shared setup – not part of the learning content."""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

WORKSHOP_ROOT = Path(__file__).resolve().parents[2]
PHASE_DIR = Path(__file__).resolve().parent

# Load shared workshop settings first, then let a phase-local `.env` override them.
load_dotenv(WORKSHOP_ROOT / ".env")
load_dotenv(PHASE_DIR / ".env", override=True)


def build_model() -> ChatOpenAI:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GITHUB_TOKEN.")
    return ChatOpenAI(
        model=os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"),
        api_key=token,
        base_url=os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference"),
        temperature=0,
    )
