# Phase 3 - Tool Usage

This phase lets the model call local Java tools.

## What Happens In This Phase

Active concepts from `WorkshopPhase`:

- `chat`
- `memory`
- `tool`

- deterministic capability
- tool invocation record
- separation between language understanding and exact execution

Included demo tools:

- calculator
- current Berlin time

What participants should notice:

- the model decides when a tool is useful
- the debug panel shows arguments and results
- tool usage changes capability more than prompt phrasing alone

## Relevant Source Code

Reading guide from `WorkshopPhase`:

- [`LangChain4jWorkshopAgentService.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/LangChain4jWorkshopAgentService.java)
- [`WorkshopTools.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopTools.java)
- [`ToolCallView.java`](../../backend/src/main/java/dev/meierhoff/agents/workshop/debug/ToolCallView.java)

The important assistant setup is:

```java
this.phase3Assistant = AiServices.builder(WorkshopAssistants.SessionAssistant.class)
        .chatModel(dependencies.chatModel())
        .chatMemoryProvider(dependencies.memory())
        .systemMessageProvider(memoryId -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_3_TOOL))
        .tools(workshopTools)
        .beforeToolExecution(this::beforeToolExecution)
        .afterToolExecution(this::afterToolExecution)
        .build();
```

What changed compared to phase 2:

- `.tools(workshopTools)` makes Java methods callable by the model
- `beforeToolExecution(...)` and `afterToolExecution(...)` feed the debug panel

The tool methods themselves are intentionally simple and visible:

```java
@Tool("Returns the current time in Europe/Berlin as a workshop-friendly string.")
String currentTime() { ... }

@Tool("Calculates a result from two numbers using add, subtract, multiply, or divide.")
double calculator(double left, double right, String operation) { ... }
```

This is the main teaching point:

- the model still decides what to do
- but exact execution is delegated to normal Java code
- the system has moved from pure text generation toward real capability
