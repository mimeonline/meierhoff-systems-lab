# Multi-Agent Systems with LangGraph

This workshop explains how multi-agent architecture patterns map to concrete LangGraph implementations. It is designed for guided learning, live coding, and architecture discussions.

## Goal

Understand multi-agent architecture through small, runnable examples:

- orchestrator
- router
- specialist agents
- shared blackboard state
- directed pipeline
- human interrupt and resume

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r phases/requirements.txt
cp .env.example .env
```

Fill `LLM_API_TOKEN` in `.env`.

## Start the Slides

```bash
npm install
npm run slides
```

## Start the App

```bash
streamlit run phases/app.py
```

The Streamlit app contains one central interface for all workshop phases. Each phase exports a `run_graph(user_input: str) -> str` function and keeps the graph logic inside its own `graph.py`.
