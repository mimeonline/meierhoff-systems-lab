# Phase 2 Chat With Memory

This phase extends the plain chat example by keeping conversation history and sending it back to the model on each turn.

## What The Code Does

The app stores prior user and assistant messages in the Chainlit session. Each new model call includes that history, which allows the model to respond with conversational continuity.

## What Changed Compared To The Previous Phase

Compared to phase 1, this version now stores and reuses prior conversation messages. The application is still a chat app, but it is no longer stateless across turns.

## Didactic Delta

- What was added: conversation memory in the current chat session
- What stayed the same: the same Chainlit app, the same model, and no tool usage
- What behavior changed: follow-up questions can build on earlier turns
- Why this matters for understanding agents: participants can feel that state changes behavior, even before any external capability is introduced

## What Participants Should Observe

- Follow-up questions work better
- The model can refer to things said earlier in the conversation
- The system feels more coherent, even though it still has no external tool access

## What Memory Means Here

In this workshop, memory means carrying forward previous conversation messages. It is not a separate database or long-term storage system. It is simply prior context that the model can use when producing the next response.

## Why Memory Matters

- The model can refer back to earlier turns
- Follow-up questions become easier to handle
- The interaction starts to feel less stateless

Memory improves continuity, but it still does not give the system new capabilities. The model still cannot search local files or use tools.

## Limitation That Still Exists

The model still cannot inspect anything outside the conversation itself. It only has memory, not new capabilities.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export GITHUB_TOKEN=your_github_token
chainlit run app.py -w
```

Optionally set `GITHUB_MODEL` to override the default model.
