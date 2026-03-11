# 🛠️ Phase 3 Chat With Tool

This phase adds a local tool named `search_knowledge(query)` to the chat application.

## 🧠 What The Code Does

The app still keeps conversation history, but the model can now decide whether it needs the local knowledge search tool. The tool reads a small Markdown knowledge base and returns a short text result for the model to use in its final answer.

## 🔄 What Changed Compared To The Previous Phase

Compared to phase 2, this version adds one capability outside the model itself. The application now contains a tool function and a loop that executes tool calls before the final answer is returned.

## 🎓 Didactic Delta

- What was added: the `search_knowledge(query)` tool and the tool-execution loop
- What stayed the same: the chat interface, the model, and conversation memory
- What behavior changed: the model can decide to consult local knowledge before answering
- Why this matters for understanding agents: this is where participants feel the shift from memory-aware chat to tool-augmented behavior

## 👀 What Participants Should Observe

- The model may answer directly or decide to call the tool
- Tool use changes the flow from one-step response to a small reasoning loop
- Answers can now reflect local workshop content from Markdown files

## 🚀 Why Tools Expand Capability

Without tools, the model can only answer from its prompt and prior messages. With tools, the model can inspect information that lives outside the model itself.

In this phase, the outside capability is intentionally simple:

- a local Markdown knowledge base
- lightweight keyword matching
- concise text returned to the model

## 🤔 How The LLM Decides To Call The Tool

The tool is bound to the model through LangChain. When the model decides that the tool would help answer the user request, it emits a tool call. The application executes that tool and returns the result to the model, which then writes the final response.

This is the key architectural shift toward agent behavior.

## ⚠️ Limitation That Still Exists

The tool is directly integrated into the application. The capability works, but the interface is still application-specific rather than standardized.

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
- `Summarize it in one sentence.`

Observe that the model may choose to use the local knowledge tool before answering. The visible behavior is still chat, but the internal flow can now include tool calls.
