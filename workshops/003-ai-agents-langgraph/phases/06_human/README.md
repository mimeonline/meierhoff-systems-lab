# Phase 06: Human

This phase demonstrates a human-in-the-loop checkpoint. A low confidence score triggers a LangGraph interrupt. The workshop app simulates the human response and resumes the graph.

## Pattern

```text
START -> assess -> human_review -> respond -> END
             \------------------> respond -> END
```

The important part is architectural: uncertainty is explicit state, and the graph can pause before continuing.
