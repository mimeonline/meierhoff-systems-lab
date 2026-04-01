# Phase 5 - RAG

This phase introduces local knowledge retrieval.

## What Happens In This Phase

Active concepts from `WorkshopPhase`:

- `chat`
- `memory`
- `rag`

- embeddings
- vector search
- context injection
- source-aware answers

What participants should notice:

- generic chat does not know workshop-local facts reliably
- retrieval pulls in the relevant markdown snippets
- answers can now reference workshop file names

## Relevant Source Code

Reading guide from `WorkshopPhase`:

- [`LangChain4jWorkshopAgentService.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/LangChain4jWorkshopAgentService.java)
- [`WorkshopPrompts.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopPrompts.java)
- [`KnowledgeBase.java`](../../backend/src/main/java/dev/meierhoff/agents/internal/KnowledgeBase.java)
- [`RetrievalView.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/debug/RetrievalView.java)
- [`knowledge/`](../../knowledge/)

The core RAG flow is in one method:

```java
private String invokeRagAssistant(String sessionId, String message) {
    List<KnowledgeBase.RetrievedChunk> chunks = runtime.knowledgeBase().retrieve(message, 3);
    String retrievalContext = chunks.stream()
            .map(chunk -> "[" + chunk.source() + "] " + chunk.text())
            .reduce((left, right) -> left + System.lineSeparator() + System.lineSeparator() + right)
            .orElse("No relevant workshop notes were found.");

    String augmentedMessage = WorkshopPrompts.ragAugmentation(message, retrievalContext);
    return InvocationScope.with(WorkshopPhase.PHASE_5_RAG, sessionId, () -> phase5Assistant.chat(sessionId, augmentedMessage));
}
```

How to read this:

- retrieve the most relevant text chunks from the local knowledge base
- build a context block from those chunks
- add that context to the user message
- send the augmented prompt to the assistant

The prompt augmentation is visible on purpose:

```java
static String ragAugmentation(String userMessage, String retrievalContext) {
    return """
            Answer the user using the retrieved workshop context when it helps.
            Make the source influence visible by mentioning file names inline.
            ...
            """.formatted(retrievalContext, userMessage);
}
```

This is the key insight of the phase:

- the model itself has not become smarter
- the application has changed the information available at answer time
- that is why local workshop facts suddenly become answerable

Suggested prompts:

```text
How is this Java workshop positioned against the earlier Python workshop?
```

```text
Why is normal chat not enough for this workshop context?
```
