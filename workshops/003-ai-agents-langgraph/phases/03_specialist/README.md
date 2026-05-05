# Phase 03: Specialist

This phase separates orchestration from specialist work. The orchestrator decides who should handle the request, then a focused specialist node produces the answer.

## Pattern

```text
START -> orchestrator -> math_agent -> END
                    -> text_agent -> END
```

Specialists keep prompts, responsibilities, and later tool access bounded by role.
