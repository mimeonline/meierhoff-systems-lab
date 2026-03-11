# 🔌 Phase 4 Chat With Tool And MCP

This phase moves the knowledge search capability behind a tiny MCP server.

## 🧠 What The Code Does

The app still behaves like the tool phase, but it no longer calls the search function directly. Instead, it starts a local MCP server process, discovers the available tool, and calls that tool through the MCP client session.

## 🔄 What Changed Compared To The Previous Phase

Compared to phase 3, the capability is no longer wired directly into the chat application. The same knowledge search is now exposed through a small MCP server and reached through an MCP client boundary.

## 🎓 Didactic Delta

- What was added: a tiny MCP server plus MCP-based tool discovery and invocation
- What stayed the same: the same knowledge-search capability, the same chat UI, and the same memory-aware interaction pattern
- What behavior changed: user-facing behavior can remain similar while the tool boundary becomes standardized
- Why this matters for understanding agents: participants can see that agent capability and tool protocol are related but not identical architectural concerns

## 👀 What Participants Should Observe

- The behavior can stay similar even when the integration pattern changes
- The app can discover and invoke a tool through MCP
- Standardized tool access changes architecture more than user-facing behavior

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
export GITHUB_TOKEN=your_github_token
env -u DEBUG chainlit run app.py -w
```

Optionally set `GITHUB_MODEL` to override the default model.

You only need to create the virtual environment once per phase directory. In a new terminal session, reactivate it with `source .venv/bin/activate`.

Running `deactivate` before switching phases is optional. It is only needed if another virtual environment is still active in your current shell and you want to avoid confusion.

## 💡 Try In Chat

After the app starts, enter:

- `What is MCP?`
- `How did you get that information?`

Observe that the user-facing answer can look similar to phase 3 even though the capability now sits behind an MCP boundary instead of a directly wired application tool.
