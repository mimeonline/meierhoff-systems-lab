---
theme: default
title: LangChain4j Overview
info: |
  A short overview of LangChain4j: capabilities, boundaries, maturity, and how it fits into the Java AI landscape.
layout: cover
class: text-center
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: JetBrains Mono
---

<style src="./theme.css"></style>

<div class="cover-content">

<div class="cover-glow"></div>

# LangChain4j Overview

<p class="subtitle">Capabilities · Limits · Maturity · Java vs Python</p>

<div class="cover-meta">
<div class="meta-item">10 to 15 minutes</div>
<div class="meta-item">Java AI landscape</div>
<div class="meta-item">Reality check included</div>
</div>

<p class="cover-footer">Meierhoff Systems Lab</p>

</div>

---
transition: fade-out
layout: two-cols
layoutClass: gap-8
---

## Why Now?

LLM capabilities are no longer optional for most product teams. The question is no longer _if_, but _how_.

- Enterprise systems are Java — most teams do not want to rewrite in Python
- Models are capable enough today for real production use cases
- Tooling has matured: memory, tools, RAG, and MCP are stable building blocks
- The cost of "wait and see" is growing

::right::

<div class="stack-card">

### The Java AI question

Most Java shops now face the same problem:

> "We need to add LLM features to our existing system. What do we actually use?"

LangChain4j and Spring AI are the two realistic answers for the JVM today.

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
transition: fade-out
layout: two-cols
layoutClass: gap-8
---

## What Is LangChain4j?

- A Java-first library for building LLM-powered applications
- Gives one API surface for models, tools, memory, embeddings, retrieval, and MCP
- Works with plain Java, but also integrates with larger Java stacks
- Strong focus on developer ergonomics through `AI Services`

::right::

<div class="stack-card">

### Short positioning

- not a full Java clone of the Python LangChain ecosystem
- more than a model client
- especially strong for practical JVM application integration

</div>

<div class="agent-formula mt-8">

`Chat Model + AI Service + Tools + Memory + Retrieval`

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: center
class: text-center
---

<div class="section-heading">

# What Can It Do?

<p class="section-heading-sub">LangChain4j already covers most building blocks for modern LLM applications in Java</p>

</div>

<div class="phase-pills">
  <span class="pill pill-active">Chat Models</span>
  <span class="pill">AI Services</span>
  <span class="pill">Tools</span>
  <span class="pill">Memory</span>
  <span class="pill">RAG</span>
  <span class="pill">MCP</span>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## Core Functions

- Chat models and streaming
- Structured output into Java types
- `AI Services` as high-level application abstraction
- Tool calling with annotated Java methods
- Chat memory abstractions
- Embeddings and vector-store integrations
- RAG building blocks
- MCP integration

::right::

## Also Worth Mentioning

- broad provider support (OpenAI, Anthropic, Gemini, Ollama, …)
- in-process local embeddings
- observability via Langfuse and OpenTelemetry
- framework integrations for Spring, Quarkus, CDI
- low-level and high-level APIs side by side

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## The Most Important Idea: AI Services

- LangChain4j can turn a small Java interface into a runnable AI-facing service
- This is one of its clearest differentiators in the Java world
- It feels natural to Java developers because it uses types, annotations, and interfaces

```java
interface Assistant {
    String chat(@MemoryId String sessionId,
                @UserMessage String message);
}
```

::right::

### Tool calling with `@Tool`

Any plain Java method can become a model-accessible tool:

```java
class WeatherService {

    @Tool("Get the current temperature for a city")
    public String getTemperature(String city) {
        return weatherApi.fetch(city);
    }
}
```

<div class="note-panel mt-3">
Tools are just annotated Java methods. LangChain4j handles schema generation and dispatch automatically — no manual JSON specification needed.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## Getting Started

Add to your `pom.xml`:

```xml
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j</artifactId>
  <version>1.0.0-beta3</version>
</dependency>

<!-- provider of your choice -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-open-ai</artifactId>
  <version>1.0.0-beta3</version>
</dependency>
```

::right::

### Wire it up

```java
OpenAiChatModel model = OpenAiChatModel.builder()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .modelName("gpt-4o-mini")
    .build();

Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(model)
    .chatMemoryProvider(id ->
        MessageWindowChatMemory.withMaxMessages(10))
    .tools(new WeatherService())
    .build();
```

<div class="note-panel mt-4">
Use `langchain4j-bom` for consistent version management across multiple modules.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## High-Level vs Low-Level

### High-level

- `AI Services`
- annotations such as `@UserMessage`, `@MemoryId`, `@Tool`
- faster to read
- often best for business applications

::right::

### Low-level

- direct `ChatModel`
- explicit `ChatRequest`
- full prompt and tool specification control
- useful when you need custom orchestration

<blockquote>
LangChain4j is strongest when teams understand both layers and choose deliberately.
</blockquote>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## How RAG Works

```mermaid {scale: 0.75}
flowchart LR
  DOC[Documents] --> CHUNK[Chunking]
  CHUNK --> EMB[Embedding Model]
  EMB --> VS[(Vector Store)]

  Q[User Question] --> QEMB[Embedding Model]
  QEMB --> RET[Retrieval]
  VS --> RET
  RET --> AUG[Augmented Prompt]
  AUG --> LLM[Chat Model]
  LLM --> ANS[Answer]
```

<div class="note-panel mt-4">
RAG quality is not just a library problem. Chunking strategy, embedding model choice, retrieval parameters, and source quality all shape the final answer.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## What Is MCP?

**Model Context Protocol** — an open standard for connecting models to external tools and data sources.

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

### Without MCP

- each integration is custom-built per application
- tools are hardcoded and not reusable across models
- no standard for capability discovery or declaration

</div>
<div>

### With MCP

- models connect to any MCP-compatible server
- tools are declared and discovered at runtime
- works across providers and frameworks

</div>
</div>

<div class="note-panel mt-6">
LangChain4j supports MCP clients out of the box. Your AI Service can consume any MCP server — local or remote — without writing custom integration code.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## What It Does Well

- Fits naturally into Java codebases
- Keeps APIs relatively understandable
- Makes tool calling and memory approachable
- Good for enterprise integration use cases
- Good fit for teams that want LLM features without moving to Python
- Supports plain Java, not only framework-based development

<div class="note-panel mt-6">
Its sweet spot is often: "We already run Java in production and want to add LLM capabilities responsibly."
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## What It Does Not Do As Well

### Compared to Python LangChain / LangGraph

- smaller ecosystem
- fewer tutorials and community recipes
- fewer battle-tested multi-agent patterns
- less mindshare for cutting-edge agent orchestration

::right::

### Practical consequence

- great for LLM applications on the JVM
- less obvious as the default choice for very complex durable agent workflows
- some architecture patterns still need to be designed more manually

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## What It Is Not

- not the Java equivalent of the full LangChain + LangGraph + LangSmith stack
- not a magic "agent framework" that solves orchestration by itself
- not automatically better than simpler direct model usage

<div class="agent-formula mt-8">

`Library maturity != every agent pattern already solved`

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## Maturity and Production Readiness

### Current picture

- active 1.x project
- broad integration surface
- used in real Java systems
- documentation is solid and practical

::right::

### Honest assessment

- yes, productive use is realistic today
- especially for chat, tools, memory, RAG, and MCP-enabled applications
- but not every area has the same maturity level
- model behavior and tool reliability still depend heavily on the chosen provider and model

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8 both-heads
---

## Production Reality Check

- The library can be production-ready before your agent architecture is
- RAG quality still depends on chunking, prompts, retrieval strategy, and source quality
- Tool calling quality is model-dependent
- Memory can improve continuity but also increase prompt noise
- Observability and testing matter just as much as the API choice

<div class="note-panel mt-6">
The main risk is usually not "Java vs Python". The main risk is underestimating the application architecture around the model.
</div>

::right::

## Testing Your AI Services

- Test tool methods in isolation — they are just Java methods
- Use a stub model to make integration tests deterministic
- Validate structured output deserialization explicitly
- Keep a separate evaluation harness for prompt quality

```java
ChatLanguageModel stub = (request) ->
    ChatResponse.builder()
        .aiMessage(AiMessage.from("stub response"))
        .build();

Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(stub)
    .build();
```

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Observability

Knowing what your model does in production is not optional.

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

### What to capture

- input and output tokens per request
- latency per model call
- tool invocations and their results
- memory state at each turn
- rendered prompts and system messages

</div>
<div>

### Options in the Java ecosystem

- **Langfuse** — open-source LLM observability, LangChain4j integration available
- **OpenTelemetry** — trace spans via `ChatModelListener`
- **Custom listeners** — `ChatModelListener` interface for low-level hooks

</div>
</div>

<div class="note-panel mt-4">
Instrument from day one. Debugging a prompt regression without traces is significantly harder than with them.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## What Spring AI Can Do

### Core capabilities

- chat model abstraction
- embeddings and vector stores
- structured output
- tool calling
- prompt and retrieval advisors
- MCP client and MCP server support

::right::

### Why teams choose it

- seamless Spring Boot integration
- configuration through familiar Spring patterns
- fits naturally into existing Spring Web, Security, Data, and Observability setups
- attractive when AI is one capability inside a larger Spring application

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## LangChain4j vs Spring AI

### LangChain4j

- standalone library
- works well in plain Java
- strong identity as a dedicated LLM toolkit
- `AI Services` are a very compelling abstraction

::right::

### Spring AI

- strongest inside an existing Spring ecosystem
- very attractive for Spring Boot teams
- leverages familiar Spring configuration and integration style
- often the better choice when AI is just one feature in a broader Spring platform

<div class="note-panel mt-6">
Short version: Spring AI is usually the more Spring-native choice. LangChain4j is usually the more library-centric and framework-light choice.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## How To Choose

```mermaid {scale: 0.75}
flowchart LR
  A{Using\nSpring Boot?} -->|Yes| B{AI is just one\nfeature in Spring?}
  A -->|No / Plain Java| C[LangChain4j]
  B -->|Yes| E[Spring AI]
  B -->|No, AI is the core| D{Interface-driven\nabstractions?}
  D -->|Yes| C
  D -->|No| E
```

<div class="note-panel mt-4">
Neither is wrong. The decision is mostly about where AI fits in your existing architecture, not about which library is objectively better.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Java World vs Python World

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">Python world</div>

- faster experimentation
- more community momentum
- more new agent patterns arrive first
- LangChain, LangGraph, LangSmith form a very visible ecosystem

</div>
<div>

<div class="col-heading col-heading-warm">Java world</div>

- stronger enterprise integration story
- more emphasis on maintainability and existing systems
- fewer dominant agent-native standards
- stronger need to choose architecture deliberately

</div>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Mental Map of the Ecosystems

```mermaid {scale: 0.8}
flowchart LR
  subgraph PYTHON[Python]
    LC[LangChain]
    LG[LangGraph]
    LS[LangSmith]
  end

  subgraph JAVA[Java]
    LC4J[LangChain4j]
    SAI[Spring AI]
    OBS[Langfuse / OpenTelemetry]
    APP[Application-specific orchestration]
  end
```

<div class="note-panel mt-6">
Python currently has the more unified agent ecosystem. Java has strong libraries, but the overall story is more plural and integration-driven.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## When LangChain4j Is A Good Fit

- your team is mainly Java
- you want LLM capabilities in an existing JVM system
- you need chat, tools, memory, RAG, or MCP without switching languages
- you want readable, typed application code
- you value pragmatic integration over chasing the newest agent trend

<div class="note-panel mt-8">
Teams that benefit most are those already operating Java in production who want to extend with AI features without a language switch or major architectural overhaul.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## When It May Not Be The Best Fit

- your main focus is advanced graph-based agent orchestration
- you want the largest ecosystem of examples and experiments
- your team is already fully invested in Python for AI engineering
- you need the newest agent patterns the moment they appear

<div class="note-panel mt-8">
These are not disqualifiers — just honest conditions where LangGraph or a Python-native stack would have a clearer advantage. The choice is about fit, not quality.
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: center
class: text-center
---

<div class="section-heading">

# Final Takeaways

<p class="section-heading-sub">LangChain4j is already a serious Java option, but it shines most when used for the right problem shape</p>

</div>

<div class="grid grid-cols-3 gap-6 mt-8">
  <div class="stack-card">
    <h3>Strong Today</h3>
    <p>Chat, tools, memory, RAG, MCP, Java integration</p>
  </div>
  <div class="stack-card">
    <h3>Less Mature</h3>
    <p>ecosystem breadth and complex agent orchestration vs Python</p>
  </div>
  <div class="stack-card">
    <h3>Best Lens</h3>
    <p>Use it as a practical JVM LLM toolkit, not as a mythical one-size-fits-all agent framework</p>
  </div>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>
