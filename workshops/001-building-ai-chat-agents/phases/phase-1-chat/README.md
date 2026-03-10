# Phase 1 Plain Chat

This phase contains the smallest possible workshop starting point: a Chainlit chat application backed by a GitHub Models language model.

## What The Code Does

The app sends only the current user message to the model along with a short system instruction. There is no conversation memory and no tool use.

## What Changed Compared To The Previous Phase

This is the starting point of the workshop, so there is no previous phase. It establishes the baseline behavior that later phases extend.

## Didactic Delta

- What was added: a minimal chat interface and one model call
- What stayed the same: there is no previous phase, so this is the baseline
- What behavior changed: nothing yet; this is the reference point for comparison
- Why this matters for understanding agents: participants need to feel what plain chat is before memory and tools are introduced

## What Participants Should Observe

- Each turn is handled independently
- Follow-up questions lose context
- The model can only answer from the current prompt and its built-in knowledge

## Limitations

- The model cannot remember earlier turns
- The model cannot inspect local files or external capabilities
- Every answer is based only on the current message and the built-in model context

## Why This Phase Matters

This phase gives participants a clean baseline. Later phases make it easy to see exactly what changes once memory and tools are introduced.

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
