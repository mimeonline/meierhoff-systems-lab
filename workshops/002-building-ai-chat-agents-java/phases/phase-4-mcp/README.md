# Phase 4 - MCP

This phase keeps the "tool" idea but changes the integration boundary.

## What Happens In This Phase

Active concepts from `WorkshopPhase`:

- `chat`
- `memory`
- `mcp`

- MCP client in the Java app
- tool server outside the application
- protocol-based discovery and invocation

What participants should notice:

- the model still sees tools
- the application no longer owns the tool implementation directly
- MCP is an architecture pattern, not just another method call

## Relevant Source Code

Reading guide from `WorkshopPhase`:

- [`LangChain4jWorkshopAgentService.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/LangChain4jWorkshopAgentService.java)
- [`McpSupport.java`](../../backend/src/main/java/dev/meierhoff/agents/internal/McpSupport.java)
- [`WorkshopRuntimeFactory.java`](../../backend/src/main/java/dev/meierhoff/agents/internal/WorkshopRuntimeFactory.java)

The visible phase code is very close to the local-tool phase:

```java
this.phase4Assistant = AiServices.builder(WorkshopAssistants.SessionAssistant.class)
        .chatModel(runtime.chatModel())
        .chatMemoryProvider(runtime.memoryStore())
        .systemMessageProvider(memoryId -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_4_MCP))
        .toolProvider(runtime.mcpToolProvider())
        .beforeToolExecution(this::beforeToolExecution)
        .afterToolExecution(this::afterToolExecution)
        .build();
```

What changed compared to phase 3:

- `.tools(workshopTools)` is replaced by `.toolProvider(runtime.mcpToolProvider())`
- from the workshop perspective, the model still gets tools
- architecturally, the tool implementation now lives behind an MCP boundary

The actual MCP transport and client setup are intentionally hidden in `internal`, because they are integration glue. The learning-relevant line is the single switch from direct tools to a tool provider.

Suggested prompt:

```text
Use MCP to inspect the workshop knowledge files and explain the goal of the Java workshop.
```
