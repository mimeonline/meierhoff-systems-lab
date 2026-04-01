# Phase 2 - Memory

This phase adds a sliding memory window.

Focus:

- session-aware chat
- follow-up questions
- visible memory in the debug panel

What participants should notice:

- the current prompt now includes previous turns
- the answer can refer back to names, constraints, and previous context
- memory improves continuity, not factual grounding

Suggested prompt sequence:

```text
My team works in finance and prefers plain Java.
```

```text
What workshop style would fit that team?
```
