# Phase 04: Blackboard

This phase uses shared state as a visible working context. Nodes read prior notes and add their own observations before the final response is produced.

## Pattern

```text
START -> analyze -> math_agent -> reviewer -> END
                 -> text_agent -> reviewer -> END
```

The `scratchpad` field is the blackboard. It keeps intermediate reasoning visible as structured state instead of hiding it inside prompts.
