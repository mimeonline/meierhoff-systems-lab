# Visible Learning Layer

This folder documents the concepts that participants should focus on while reading the Java backend.

The corresponding Java package is:

```text
src/main/java/dev/meierhoff/agents/workshop
```

Suggested package reading order:

- `workshop/phases`
- `workshop/core/LangChain4jWorkshopAgentService`
- `workshop/core/WorkshopAssistants`
- `workshop/core/WorkshopPrompts`
- `workshop/core/WorkshopTools`
- `workshop/api`
- `workshop/debug`

Visible concepts:

- LangChain4j AI service interfaces
- visible prompts per phase
- tool methods exposed to the model
- phase-by-phase agent composition
- RAG prompt augmentation
- isolated transport and debug records

Package intent:

- `workshop/phases`: explains what each phase activates and which source files are worth reading
- `workshop/core`: the learning-relevant LangChain4j code
- `workshop/api`: request/response records
- `workshop/debug`: debug panel records

Everything else lives in the internal implementation package.

If you want to understand the hidden infrastructure boundaries without reading
every support class, continue with `backend/internal/README.md`.
