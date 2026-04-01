# Phase 2 - Memory

This phase adds a sliding memory window.

## What Happens In This Phase

Active concepts from `WorkshopPhase`:

- `chat`
- `memory`

- session-aware chat
- follow-up questions
- visible memory in the debug panel

What participants should notice:

- the current prompt now includes previous turns
- the answer can refer back to names, constraints, and previous context
- memory improves continuity, not factual grounding

## Relevant Source Code

Reading guide from `WorkshopPhase`:

- [`LangChain4jWorkshopAgentService.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/LangChain4jWorkshopAgentService.java)
- [`WorkshopAssistants.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopAssistants.java)
- [`InspectableChatMemoryStore.java`](../../backend/src/main/java/dev/meierhoff/agents/internal/InspectableChatMemoryStore.java)

The core difference to phase 1 is this assistant definition:

```java
this.phase2Assistant = AiServices.builder(WorkshopAssistants.SessionAssistant.class)
        .chatModel(runtime.chatModel())
        .chatMemoryProvider(runtime.memoryStore())
        .systemMessageProvider(memoryId -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_2_MEMORY))
        .chatRequestTransformer((request, memoryId) -> capturePrompt(WorkshopPhase.PHASE_2_MEMORY, request.messages(), memoryId, request))
        .build();
```

What changed:

- `SessionAssistant` now includes a `sessionId`
- `chatMemoryProvider(...)` adds a memory implementation
- the rest of the code still looks very similar to phase 1

The visible interface makes the change very easy to spot:

```java
interface SessionAssistant {
    String chat(@MemoryId String sessionId, @UserMessage String userMessage);
}
```

That one extra `@MemoryId` parameter is the conceptual shift. LangChain4j uses it to connect a conversation to stored chat history.

The runtime memory implementation is hidden in `internal`, because participants mainly need to understand the architectural effect, not the storage plumbing.

Suggested prompt sequence:

```text
My team works in finance and prefers plain Java.
```

```text
What workshop style would fit that team?
```
