# Phase 04: Blackboard

This phase uses shared state as a visible working context. Nodes read and update the same `blackboard` dictionary before the final response is produced.

## Pattern

```text
START -> analyze -> math_agent -> reviewer -> END
                 -> text_agent -> reviewer -> END
```

Unlike a router, the important behavior is not the branch. Unlike the specialist phase, the important artifact is not a one-way delegation brief. The `blackboard` field is a shared workspace: `analyze` writes route and analysis, the selected specialist adds a draft, and `reviewer` reads the accumulated state to produce the final snapshot.
