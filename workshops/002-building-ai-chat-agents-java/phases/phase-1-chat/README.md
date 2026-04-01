# Phase 1 - Chat

This is the baseline. In this phase the system is only a plain LLM call: one user message goes in, one answer comes back.

## What Happens In This Phase

Active concepts from `WorkshopPhase`:

- `chat`

- `AiServices` builds a single-turn assistant
- the assistant receives only the current user message
- there is no memory, no tool usage, and no retrieval context

What participants should notice:

- the model can answer general questions
- it has no local workshop context
- follow-up questions are weak because nothing is remembered

## Relevant Source Code

Reading guide from `WorkshopPhase`:

- [`LangChain4jWorkshopAgentService.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/LangChain4jWorkshopAgentService.java)
- [`WorkshopAssistants.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopAssistants.java)
- [`WorkshopPrompts.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopPrompts.java)

The important part is the first assistant definition:

```java
this.phase1Assistant = AiServices.builder(WorkshopAssistants.SingleTurnAssistant.class)
        .chatModel(runtime.chatModel())
        .systemMessageProvider(ignored -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_1_CHAT))
        .chatRequestTransformer((request, ignored) -> capturePrompt(WorkshopPhase.PHASE_1_CHAT, request.messages(), null, request))
        .build();
```

How to read this:

- `AiServices.builder(...)` tells LangChain4j to create an AI service from a Java interface
- `SingleTurnAssistant` means there is no `sessionId` and therefore no memory
- `systemMessageProvider(...)` selects the prompt for this phase
- `chatRequestTransformer(...)` is only used for the debug view so we can inspect the prompt

The interface itself is intentionally tiny:

```java
interface SingleTurnAssistant {
    String chat(@UserMessage String userMessage);
}
```

This is the key lesson of phase 1: LangChain4j can turn a small Java interface into a runnable chat service.

Suggested prompt:

```text
What is LangChain4j and why might a Java team use it?
```
