# Phase 6 - Compare

This optional phase runs multiple variants side by side.

## What Happens In This Phase

Active concepts from `WorkshopPhase`:

- `chat`
- `comparison`

- compare output quality
- compare grounding
- compare determinism

What participants should notice:

- plain chat sounds plausible
- memory improves continuity
- tools improve exactness
- RAG improves local factual grounding

## Relevant Source Code

Reading guide from `WorkshopPhase`:

- [`LangChain4jWorkshopAgentService.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/LangChain4jWorkshopAgentService.java)
- [`ComparisonResult.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/debug/ComparisonResult.java)

The comparison phase does not introduce a new LangChain4j feature. Instead, it orchestrates several existing variants:

```java
private ChatResponsePayload compare(String sessionId, String message) {
    List<ComparisonResult> comparisons = new ArrayList<>();
    comparisons.add(compareVariant(WorkshopPhase.PHASE_1_CHAT, sessionId, message));
    comparisons.add(compareVariant(WorkshopPhase.PHASE_2_MEMORY, sessionId, message));
    comparisons.add(compareVariant(WorkshopPhase.PHASE_3_TOOL, sessionId, message));
    comparisons.add(compareVariant(WorkshopPhase.PHASE_5_RAG, sessionId, message));
    ...
}
```

Why this phase matters:

- participants can compare outputs for the same prompt
- the architectural differences become visible in one screen
- it reinforces that an "agent" is not one thing, but a combination of capabilities

This is the synthesis phase. The source code is intentionally simple because the learning value comes from comparing behaviors, not from adding another infrastructure layer.

Good discussion question:

```text
Which capability changed the answer the most for this prompt, and why?
```
