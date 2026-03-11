# 🤖 001 Building AI Chat Agents

This workshop teaches what an AI agent is by extending a simple chat application in five small phases. Participants make one architectural change at a time and observe how system behavior changes.

## 🎯 Workshop Goal

Make the evolution from plain chat to a minimal agent visible and understandable. The examples stay intentionally small and reproducible.

## 📚 Learning Goals

- Understand what an AI agent is in practical architectural terms
- See how memory changes model behavior across turns
- See how tool calling changes model behavior and capability
- Understand where MCP fits as a standardized tool interface
- Reinforce the mental model `Agent = LLM + Memory + Tools + Reasoning Loop`

## ⏱️ Duration

75 minutes

## 👥 Audience

Developers, architects, and technically curious practitioners who want a practical first model for AI agents.

## 🧰 Prerequisites

- Basic Python familiarity
- Python 3.13 installed and available as `python3.13`
- A GitHub account with access to GitHub Models
- A GitHub token available as `GITHUB_TOKEN`

Create a GitHub token before the workshop and add it to the shared workshop `.env` file. The applications use that token to authenticate against GitHub Models.

Verify before the workshop:

```bash
python3.13 --version
```

## 🗺️ Workshop Flow

| Time | Phase | Focus |
|------|-------|-------|
| 0-10 min | Intro | What an AI agent is and how the workshop is structured |
| 10-20 min | Phase 1 | Plain chat – the baseline |
| 20-30 min | Phase 2 | Add memory |
| 30-45 min | Phase 3 | Add a local tool |
| 45-55 min | Phase 4 | Connect the tool through MCP |
| 55-65 min | Phase 5 | Compare direct vs MCP side by side |
| 65-75 min | Recap | Discussion |

## 🧩 Phases

| Phase | Directory | What changes |
|-------|-----------|-------------|
| 1 | `phase-1-chat` | Plain chat, no memory, no tools |
| 2 | `phase-2-memory` | Conversation history added |
| 3 | `phase-3-tool` | Local `search_knowledge` tool |
| 4 | `phase-4-mcp` | Same tool, reached through MCP |
| 5 | `phase-5-compare` | Both paths in one agent |

Together these phases reinforce: `Agent = LLM + Memory + Tools + Reasoning Loop`

## 🚀 How To Run Each Phase

First create one shared workshop env in `workshops/001-building-ai-chat-agents/.env`:

```bash
cp .env.example .env
```

Open that `.env` file and replace `your_github_token_here` with a real GitHub token that has access to GitHub Models.

After that, from the phase directory:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
env -u DEBUG chainlit run app.py -w
```

Create `.venv` once per phase directory. In later sessions, reactivate with `source .venv/bin/activate`.

All phases load that shared `.env` automatically. If needed, a phase-local `.env` can still be added to override the shared values for that phase only.

Optionally set `GITHUB_MODEL` in `.env` to override the default model.

### 🛟 Shell Note

If your shell exports `DEBUG=release`, Chainlit can fail at startup. The `env -u DEBUG` prefix avoids that.

### 🐍 Python Version

Use Python 3.13. The current stack can have issues on Python 3.14.

## 📁 Folder Structure

```text
workshops/001-building-ai-chat-agents/
├── README.md
├── knowledge/              # shared knowledge base (used by phases 3-5)
│   ├── ai-agents.md
│   ├── mcp.md
│   └── tools.md
├── slides/
│   ├── slides.md
│   └── theme.css
├── phases/
│   ├── phase-1-chat/
│   ├── phase-2-memory/
│   ├── phase-3-tool/
│   ├── phase-4-mcp/
│   └── phase-5-compare/
├── assets/
│   └── README.md
└── follow-up/
    └── README.md
```

## 💬 Discussion Prompts

- Your company has an FAQ system – do you need an agent or does RAG suffice?
- You want to summarize emails – chat, agent, or workflow?
- At what point does a chat app become agent-like?
- What does memory add, and what does it not add?
- Why do tools change the system more than prompt wording alone?
- What is the difference between a direct tool integration and an MCP-based one?
