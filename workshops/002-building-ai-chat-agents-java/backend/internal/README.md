# Hidden Infrastructure Layer

This folder describes the backend package that workshop participants usually do not need to study in detail.

The corresponding Java package root is:

```text
src/main/java/dev/meierhoff/agents/internal
```

Subpackage intent:

- `internal/bootstrap`: application startup and dependency assembly
- `internal/config`: environment loading and path detection
- `internal/http`: REST endpoints and static frontend serving
- `internal/debug`: support classes for the debug panel
- `internal/model`: provider-specific `ChatModel` creation
- `internal/mcp`: MCP transport and client wiring
- `internal/memory`: inspectable memory implementation
- `internal/rag`: knowledge loading, chunking, embeddings, retrieval
- `internal/support`: small technical helpers such as prompt formatting

Reading advice:

- Skim this package to understand system boundaries.
- Do not start here if your goal is to learn LangChain4j concepts.
- Start with `backend/workshop/README.md` and the `workshop/*` packages first.

Why this package is hidden:

- It contains setup and runtime glue.
- It makes the workshop runnable on a local machine.
- It does not add much conceptual value for the phase-by-phase agent learning journey.
