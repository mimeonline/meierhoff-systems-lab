# Phase 05: Pipeline

This phase uses a fixed sequence rather than dynamic delegation. It is useful when the process is known and should remain predictable.

## Architecture question

Which order is fixed?

## Pattern

```text
START -> analyze -> process -> respond -> END
```

A pipeline is often the right answer before introducing more agents.
