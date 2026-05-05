# Phase 03: Specialist

This phase separates orchestration from specialist work. The orchestrator creates an explicit delegation brief, sends it to the right specialist, and reviews the specialist output before returning the result.

## Architecture question

Who handles which role?

## Pattern

```text
START -> orchestrator -> math_agent -> orchestrator_review -> END
                    -> text_agent -> orchestrator_review -> END
```

Unlike a router, the orchestrator does more than choose a branch: it defines the role, responsibility, and expected output for the specialist. Specialists keep prompts, responsibilities, and later tool access bounded by role.
