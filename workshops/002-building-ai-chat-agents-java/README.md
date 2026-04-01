# 002 Building AI Chat Agents in Java

This workshop shows how to build an AI agent in plain Java with LangChain4j, without Spring Boot or Quarkus. The goal is not framework fluency. The goal is to make the architecture visible.

Participants can move through a small sequence of phases and see how the system changes when we add memory, tools, MCP, and retrieval.

## Workshop Goal

Build a locally runnable workshop project that makes this progression understandable:

```text
plain chat -> memory -> tool usage -> MCP -> RAG -> comparison
```

The visible learning layer stays in the `workshop` package. Infrastructure, model wiring, JSON, MCP setup, and retrieval indexing stay in `internal`.

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
│   ├─ WorkshopPhase                                                     │
│   ├─ WorkshopAgentService                                              │
│   └─ DTOs for chat and debug                                           │
│                                                                       │
│ internal package                                                       │
│   ├─ model factory                                                     │
│   ├─ memory store                                                      │
│   ├─ local tools                                                       │
│   ├─ MCP client setup                                                  │
│   ├─ knowledge embeddings + retrieval                                  │
│   └─ debug capture                                                     │
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

## Didactic Design

The important teaching split is:

### Visible

- `WorkshopPhase`
- `WorkshopAgentService`
- request and debug DTOs
- the conceptual phase progression

### Hidden

- model provider setup
- HTTP server and JSON mapping
- MCP transport wiring
- prompt capture
- embedding model and in-memory vector store

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

## Optional Dockerfile

There is a simple backend Dockerfile for container-based demos. It is intentionally small and leaves model credentials to runtime environment variables.

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
