# Phase 01: Orchestrator

This baseline uses one graph and one node. It shows the smallest useful LangGraph structure before introducing routing or multiple roles.

## Architecture question

Who keeps the flow together?

In this phase the answer is intentionally small: one graph node owns the whole flow so later phases have a clear baseline.

## Pattern

```text
START -> assistant -> END
```

## Run

Use the central app:

```bash
streamlit run phases/app.py
```
