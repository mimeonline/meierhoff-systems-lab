# Workshop Phases

Each phase is a small, runnable LangGraph example. The central Streamlit app imports the selected phase dynamically and calls:

```python
def run_graph(user_input: str) -> str
```

## Run

```bash
streamlit run phases/app.py
```

## Phases

- `01_orchestrator`: one graph, one node, direct answer
- `02_router`: conditional routing to math or text
- `03_specialist`: orchestrator plus specialist nodes
- `04_blackboard`: shared state as visible working context
- `05_pipeline`: fixed analyze, process, respond flow
- `06_human`: interrupt and simulated resume when confidence is low
