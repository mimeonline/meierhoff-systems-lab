# Phase 02: Router

This phase adds a routing decision. The router writes a `route` value into state and a conditional edge sends the request to the right node.

## Pattern

```text
START -> router -> math_agent -> END
                -> text_agent -> END
```

The route is intentionally simple and readable so the architecture stays visible.
