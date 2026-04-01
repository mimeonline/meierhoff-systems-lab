# Tool Usage vs MCP

Direct tool usage means the application exposes Java methods to the model.

That is ideal when:

- the tool is local
- the implementation is small
- the team owns the code directly
- the workshop wants maximum clarity

MCP is different. MCP standardizes how a model-facing application can discover and call tools from an external server.

That is useful when:

- the tool lives outside the application
- multiple clients should use the same tool surface
- the integration boundary itself is part of the lesson

For this workshop, the important teaching message is:

- direct tool usage shows the simplest path
- MCP shows the standard protocol path

Participants should see that both expose capabilities to the model, but the ownership and integration story are different.
