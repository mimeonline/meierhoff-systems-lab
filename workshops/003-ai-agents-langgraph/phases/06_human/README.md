# Phase 06: Human

This phase demonstrates a human-in-the-loop checkpoint. A low confidence score triggers a LangGraph interrupt before the final response. The workshop app simulates the human response and resumes the graph.

## Architecture question

Where must a human intervene?

## Pattern

```text
START -> assess -> human_review interrupt/resume -> respond -> END
             \------------------> respond -> END
```

The important part is architectural: uncertainty is explicit state, and the graph can pause at a visible intervention point before continuing. In this example the human must clarify the assumption the assistant should use before `respond`.
