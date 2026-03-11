# 🔌 Phase 4 Chat With Tool And MCP

This phase lets participants compare two paths to the same capability: a direct local tool call and an MCP-backed tool loaded into LangChain through an adapter.

## 🧠 What The Code Does

The app exposes both a direct local tool and an MCP-backed version of the same knowledge search. It starts a local MCP server process, discovers the available MCP tool, loads it into LangChain through `langchain-mcp-adapters`, and lets the model choose between the direct path and the MCP path.

The file responsibilities are intentionally split:

- `tools.py`: shared knowledge-search capability
- `mcp_server.py`: MCP exposure layer for that capability
- `app.py`: direct tool path, MCP startup/discovery, adapter loading, and agent orchestration

## 🔄 What Changed Compared To The Previous Phase

Compared to phase 3, the same knowledge search can now be reached in two ways: directly in the app or through a small MCP server and adapter boundary.

## 🎓 Didactic Delta

- What was added: a tiny MCP server plus adapter-based MCP tool loading alongside the original direct tool path
- What stayed the same: the same knowledge-search capability, the same chat UI, and the same memory-aware interaction pattern
- What behavior changed: participants can now compare a direct tool call with an MCP-backed tool call in the same phase
- Why this matters for understanding agents: participants can see that capability and transport boundary are separate architectural concerns

## 👀 What Participants Should Observe

- The same knowledge can be reached through a direct tool call or through MCP
- The app can discover an MCP tool and load it into LangChain through an adapter
- The Chainlit UI shows which path was used because the tool names are different
- Standardized tool access changes architecture more than the knowledge content itself

## 🧩 What MCP Is

MCP stands for Model Context Protocol. It is a standard protocol for exposing tools and related capabilities to models and agent systems.

## 🏗️ Why Standardized Tool Protocols Matter

- They separate capabilities from application-specific integration code
- They make discovery and invocation more consistent
- They reduce custom adapters when more tools are introduced

In this workshop, the capability stays intentionally simple: local Markdown knowledge search. The architectural lesson is the protocol boundary, not the complexity of the tool.

## ⚠️ Limitation That Still Exists

This is a workshop-scale MCP integration. It is intentionally small and local so the protocol idea is understandable. It is not a full production tool platform.

## 🚀 Run

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
env -u DEBUG chainlit run app.py -w
```

Optionally set `GITHUB_MODEL` to override the default model.

You do not need to start `mcp_server.py` manually. `app.py` launches the local MCP server automatically over stdio during discovery and agent execution.

You only need to create the virtual environment once per phase directory. In a new terminal session, reactivate it with `source .venv/bin/activate`.

Running `deactivate` before switching phases is optional. It is only needed if another virtual environment is still active in your current shell and you want to avoid confusion.

## 💡 Try In Chat

After the app starts, enter:

- `Use the direct tool to explain MCP.`
- `Use MCP to explain MCP.`
- `Compare both paths for the same question.`

Observe that the returned knowledge can stay similar while the architecture differs.

Also observe the visible tool steps in the Chainlit UI:

- `search_knowledge_direct` means a direct local Python tool call
- `search_knowledge_mcp` means the call went through the MCP server and adapter

Also watch the terminal logs:

- direct path logs stay inside the application/tool layer
- MCP path logs show server startup, discovery, adapter loading, and MCP session activity
