# 🤖 001 Building AI Chat Agents

This workshop teaches what an AI agent is by extending a simple chat application in four small phases. Participants make one architectural change at a time and observe how system behavior changes.

## 🎯 Workshop Goal

The goal is to make the evolution from plain chat to a minimal agent visible and understandable. The examples stay intentionally small and reproducible.

## 📚 Learning Goals

- Understand what an AI agent is in practical architectural terms
- See how memory changes model behavior across turns
- See how tool calling changes model behavior and capability
- Understand where MCP fits as a standardized tool interface
- Reinforce the mental model `Agent = LLM + Tools + Reasoning Loop`

## ⏱️ Duration

60 minutes

## 👥 Audience

This session is aimed at developers, architects, and technically curious practitioners who want a practical first model for AI agents.

## 🧰 Prerequisites

- Basic Python familiarity
- Python 3.13 installed and available as `python3.13`
- A GitHub account with access to GitHub Models
- A GitHub token available as `GITHUB_TOKEN`

Before the workshop, verify the Python runtime:

```bash
python3.13 --version
```

If this command fails, install Python 3.13 first and only then continue with the workshop setup.

## 🗺️ Workshop Flow

- 0-10 min: what an AI agent is and how the workshop is structured
- 10-20 min: phase 1, plain chat
- 20-30 min: phase 2, add memory
- 30-45 min: phase 3, add a local tool
- 45-55 min: phase 4, connect the tool through MCP
- 55-60 min: recap and discussion

## 🧩 Phases

- `phase-1-chat`: a plain chat app with no memory and no tools
- `phase-2-memory`: the same app with conversation history
- `phase-3-tool`: the chat app can call a local `search_knowledge` tool
- `phase-4-mcp`: the knowledge search is exposed through a tiny MCP server

Together these phases reinforce the mental model:

`Agent = LLM + Tools + Reasoning Loop`

Memory helps the system stay coherent across turns. Tools let the model act on information outside its built-in context. MCP shows how tools can be provided through a standardized protocol boundary.

## 👀 What Participants Should Feel Across The Phases

- Plain chat feels stateless. Each turn stands alone.
- Memory-aware chat feels continuous. The model can follow the conversation.
- Tool-augmented chat feels more capable. The model can reach beyond the prompt.
- MCP-enabled tool usage feels architecturally cleaner. The capability stays similar, but the interface becomes standardized.

This progression is deliberate. The workshop is designed to make the behavioral and architectural differences noticeable rather than merely described.

## 🏗️ Architecture Overview

The workshop keeps the request flow intentionally visible:

`User -> Chainlit UI -> LLM -> optional memory -> optional tool decision -> tool execution -> result returned to LLM -> final answer`

In phase 4, MCP sits between the application and the capability provider:

`LLM application -> MCP client -> MCP server -> knowledge search capability`

## 🛠️ What Participants Will Build

Participants will build and run four small versions of the same chat application:

- a plain LLM chat
- a chat that remembers previous turns
- a chat that can call a local knowledge-search tool
- a chat that reaches the same capability through MCP

The tool demonstration uses a small local Markdown knowledge base rather than an external API so the example stays reproducible and easy to inspect.

## 📁 Folder Structure

```text
workshops/001-building-ai-chat-agents/
├── README.md
├── slides/
│   ├── slides.md
│   └── theme.css
├── phases/
│   ├── phase-1-chat/
│   ├── phase-2-memory/
│   ├── phase-3-tool/
│   └── phase-4-mcp/
├── assets/
│   └── README.md
└── follow-up/
    └── README.md
```

## 🚀 How To Run Each Phase

Each phase is self-contained. From the phase directory you want to run:

```bash
python3.13 --version
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
env -u DEBUG chainlit run app.py -w
```

Create `.venv` once per phase directory. In later terminal sessions, reactivate it with `source .venv/bin/activate`.

If you want a different model, also export `GITHUB_MODEL` or set it in `.env`. Each phase README includes notes about what to look for in the chat and what behavior to compare.

## 💬 Discussion Prompts

- At what point does a chat app become agent-like?
- What does memory add, and what does it not add?
- Why do tools change the system more than prompt wording alone?
- What is the difference between a direct tool integration and an MCP-based one?
- Which parts of these examples are architectural, and which are just implementation details?

## 📝 Note

The workshop examples are deliberately minimal and educational. They are designed to make behavior and architecture visible rather than to model production systems.
