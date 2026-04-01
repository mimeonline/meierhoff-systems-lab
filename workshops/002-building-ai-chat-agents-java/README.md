# 002 Building AI Chat Agents in Java

This workshop shows how to build an AI agent in plain Java with LangChain4j, without Spring Boot or Quarkus. The goal is not framework fluency. The goal is to make the architecture visible.

Participants can move through a small sequence of phases and see how the system changes when we add memory, tools, MCP, and retrieval.

This repository can also be used for self-study. If you are not following a live presenter, the phase guides in `phases/` are the step-by-step path through the workshop.

## Workshop Goal

Build a locally runnable workshop project that makes this progression understandable:

```text
plain chat -> memory -> tool usage -> MCP -> RAG -> comparison
```

The visible learning layer stays in the `workshop` package. Infrastructure, model wiring, JSON, MCP setup, and retrieval indexing stay in `internal`.

## What Participants Should Read

Workshop participants do not need to understand the whole backend. The intended reading path is:

1. [`LangChain4jWorkshopAgentService.java`](./backend/src/main/java/dev/meierhoff/agents/workshop/core/LangChain4jWorkshopAgentService.java)
2. [`WorkshopAssistants.java`](./backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopAssistants.java)
3. [`WorkshopPrompts.java`](./backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopPrompts.java)
4. [`WorkshopTools.java`](./backend/src/main/java/dev/meierhoff/agents/workshop/core/WorkshopTools.java)
5. the phase guides in [`phases/`](./phases/)

These files contain the learning-relevant LangChain4j code:

- how AI services are defined
- how memory changes the assistant
- how tools are exposed
- how MCP replaces direct tool wiring
- how RAG augments the prompt

Participants can safely ignore most files in `backend/internal/`. Those files mainly exist so the workshop can run locally without distracting from the core concepts.

If you want a quick orientation for the hidden glue layer, see `backend/internal/README.md`.

## Self-Study Mode

This workshop is designed so you can work through it on your own.

If there is no presenter guiding you, use the phase guides in [`phases/`](./phases/) as the primary workshop script. They are not secondary notes. They are the guided learning path for self-study.

Recommended self-study flow:

1. complete the setup and start the application locally
2. open the UI and keep the debug panel visible
3. start with [`phases/phase-1-chat/README.md`](./phases/phase-1-chat/README.md)
4. work through each phase in order up to [`phases/phase-6-compare/README.md`](./phases/phase-6-compare/README.md)
5. for each phase:
   read the phase README first
   run the suggested prompts in the UI
   inspect `/debug` output in the frontend
   open the linked source files and compare the code with the previous phase

What the phase READMEs are for:

- they explain what changes in the phase
- they point to the exact source files worth reading
- they show the relevant code snippet
- they help you "play through" the workshop without needing a live explanation

## Audience

- Java developers
- software architects
- AI engineers who want a plain-Java mental model

## Tech Stack

- Plain Java
- Java 25 preferred for local development
- Java 21 as the documented compatibility baseline for the Maven build
- Maven
- LangChain4j
- Plain HTML
- TypeScript
- TailwindCSS

## Folder Structure

```text
workshops/002-building-ai-chat-agents-java/
├── README.md
├── .env.example
├── knowledge/
├── slides/
│   ├── slides.md
│   └── package.json
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
├── backend/
│   ├── pom.xml
│   ├── workshop/
│   ├── internal/
│   └── src/main/java/dev/meierhoff/agents/
└── phases/
    ├── phase-1-chat/
    ├── phase-2-memory/
    ├── phase-3-tool/
    ├── phase-4-mcp/
    ├── phase-5-rag/
    └── phase-6-compare/
```

## Architecture

```text
┌─────────────────────────────── frontend ───────────────────────────────┐
│ plain HTML + TypeScript + Tailwind                                    │
│                                                                       │
│ chat area                         debug inspector                     │
│ user message -> POST /chat       <- prompt, memory, tools, retrieval  │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────── backend ───────────────────────────────────┐
│ WorkshopHttpServer                                                     │
│   ├─ POST /chat                                                        │
│   └─ GET /debug                                                        │
│                                                                       │
│ workshop package                                                       │
│   ├─ LangChain4jWorkshopAgentService                                   │
│   ├─ WorkshopAssistants                                                │
│   ├─ WorkshopPrompts                                                   │
│   ├─ WorkshopTools                                                     │
│   └─ DTOs for chat and debug                                           │
│                                                                       │
│ internal package                                                       │
│   ├─ HTTP server                                                       │
│   ├─ environment loading                                               │
│   ├─ model factory                                                     │
│   ├─ MCP client setup                                                  │
│   ├─ retrieval index                                                   │
│   └─ debug/runtime plumbing                                            │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        Chat Model         MCP Server         Knowledge Base
     GitHub Models or       filesystem        local markdown files
         Ollama              tools            embedded in-memory
```

## Setup

### 1. Prerequisites

- Java 25 preferred, Java 21 minimum
- Maven 3.9+
- Node.js 20+ and npm
- one chat model provider:
  - GitHub Models with a PAT that has `models` scope
  - or Ollama running locally

### 2. Configure the environment

Create a workshop-local `.env` file in `workshops/002-building-ai-chat-agents-java/`:

```bash
cp .env.example .env
```

The backend loads this file automatically. A second optional `backend/.env` can override values locally for backend-only experiments.

Example for GitHub Models:

```bash
GITHUB_TOKEN=your_token_with_models_scope
GITHUB_MODEL=openai/gpt-4.1-mini
GITHUB_MODELS_BASE_URL=https://models.github.ai/inference
```

Example for Ollama:

```bash
WORKSHOP_MODEL_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

### 3. Build the frontend

```bash
cd frontend
npm install
npm run build
```

### 4. Start the backend

Open a second terminal:

```bash
cp .env.example .env
cd backend
mvn -Dmaven.repo.local=.m2 compile exec:java
```

Then open:

```text
http://localhost:8080
```

## API

### `POST /chat`

Request:

```json
{
  "phase": "phase-3-tool",
  "sessionId": "demo-session",
  "message": "What time is it in Berlin?"
}
```

Response:

```json
{
  "sessionId": "demo-session",
  "phase": "phase-3-tool",
  "answer": "...",
  "comparisons": []
}
```

### `GET /debug`

```text
GET /debug?phase=phase-5-rag&sessionId=demo-session
```

The response includes:

- current prompt
- memory snapshot
- recorded tool calls
- retrieved RAG chunks
- comparison outputs for phase 6

## Phases

### Phase 1 - Chat

Baseline chat with an LLM and no memory.

### Phase 2 - Memory

Adds a sliding window memory so follow-up questions can reuse prior turns.

### Phase 3 - Tool

Adds local Java tools for deterministic work such as time and calculation.

### Phase 4 - MCP

Reaches tools through an MCP client instead of direct Java methods. This makes the "tool bridge" idea visible.

### Phase 5 - RAG

Uses local workshop notes in `knowledge/` with embeddings and retrieval. This phase is designed so participants can ask workshop-specific questions that plain chat usually cannot answer reliably.

### Phase 6 - Compare

Runs several variants side by side so participants can compare what changed.

Each phase folder contains:

- what changes conceptually
- which source files participants should read
- a small code excerpt with explanation

If you are doing this as self-study, these phase folders are the main workshop path.

## Didactic Design

The important teaching split is:

### Visible

- `LangChain4jWorkshopAgentService`
- `WorkshopAssistants`
- `WorkshopPrompts`
- `WorkshopTools`
- `WorkshopPhase`
- request and debug DTOs
- the phase documentation in `phases/`

### Hidden

- environment loading
- model provider setup
- HTTP server and JSON mapping
- MCP transport wiring
- retrieval index implementation
- debug/runtime plumbing

Rule of thumb:

- if a file teaches how LangChain4j changes the system, it belongs in `workshop`
- if a file mainly helps the application boot, connect, parse, or store, it belongs in `internal`

## RAG Design Notes

The local knowledge base contains workshop-specific facts that a generic model usually does not know:

- HH Nerd Gruppe context
- how this Java workshop differs from the earlier Python workshop
- exact framing of the workshop goals
- positioning of LangChain4j and Spring AI

That lets participants observe:

- why plain chat is weak on local, niche facts
- why retrieval helps
- how file names and snippets influence the answer

## Slides

Slides live in [slides/slides.md](/Users/michaelmeierhoff/Code/projects/msys/meierhoff-systems-lab/workshops/002-building-ai-chat-agents-java/slides/slides.md) and can be run with Slidev from the [slides/README.md](/Users/michaelmeierhoff/Code/projects/msys/meierhoff-systems-lab/workshops/002-building-ai-chat-agents-java/slides/README.md) workflow.

## Suggested Workshop Flow

- 10 min intro and architecture walkthrough
- 10 min phase 1
- 10 min phase 2
- 10 min phase 3
- 10 min phase 4
- 15 min phase 5
- 10 min comparison and discussion

For self-study, follow the same order, but use the phase READMEs as your facilitator.
