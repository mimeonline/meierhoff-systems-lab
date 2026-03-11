---
theme: default
title: Building AI Chat Agents with LangChain, Chainlit, GitHub Models, Tools, and MCP
info: |
  A technical workshop deck for understanding AI agents through incremental implementation phases.
layout: cover
class: text-center
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: JetBrains Mono
---

<style src="./theme.css"></style>

<div class="cover-content">

<div class="cover-glow"></div>

# Building AI Chat Agents

<p class="subtitle">LangChain &middot; Chainlit &middot; GitHub Models &middot; Tools &middot; MCP</p>

<div class="cover-meta">
<div v-click class="meta-item">60 minutes</div>
<div v-click class="meta-item">Four phases</div>
<div v-click class="meta-item">Local knowledge search</div>
</div>

<p v-click class="cover-footer">Meierhoff Systems Lab</p>

</div>

---
transition: fade-out
---

## Why This Workshop Exists

<v-clicks>

- LLM chat is often labeled an **"agent"** too early
- The useful question is: **what changed in the system?**
- This workshop adds one capability at a time
- We alternate between short explanation and live coding
- Participants compare code, behavior, and architecture after every phase

</v-clicks>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## What Is An AI Agent?

<v-clicks>

- A model alone is **not** the whole system
- Memory can preserve conversational state
- Tools extend capability beyond generation
- The key shift is a **loop**: decide, act, observe, respond

</v-clicks>

<div v-click class="agent-formula">

`Agent = LLM + Tools + Reasoning Loop`

</div>

::right::

<div v-click class="diagram-container">

```mermaid {theme: 'base', scale: 0.65}
flowchart TD
  U[User] --> UI[Chainlit UI]
  UI --> LLM[LLM]
  LLM --> M[Optional Memory]
  LLM --> D{Need a tool?}
  D -->|yes| T[Tool]
  T --> LLM
  D -->|no| A[Answer]
```

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: center
class: text-center
---

<div class="section-heading">

# The Four Phases

<p class="section-heading-sub">Each phase adds exactly one architectural change</p>

<div class="phase-pills" v-click>
  <span class="pill pill-active">Chat</span>
  <span class="pill-arrow">&rarr;</span>
  <span class="pill">Memory</span>
  <span class="pill-arrow">&rarr;</span>
  <span class="pill">Tools</span>
  <span class="pill-arrow">&rarr;</span>
  <span class="pill">MCP</span>
</div>

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Phase 1 &mdash; Plain Chat

<div class="phase-badge">Phase 1</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

<v-clicks>

- Baseline Chainlit chat
- One model call per user message

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

<v-clicks>

- No memory
- No tools
- One response step only

</v-clicks>

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

<v-clicks>

- None yet
- This is plain chat only
- Each turn stands alone

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

<v-clicks>

- This is the reference point for the workshop
- Participants can feel what the system cannot yet do
- Good moment to switch into the first live-coding step

</v-clicks>

</div>
</div>

<div v-click class="flow">
  <span class="flow-node">User</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Answer</span>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Phase 2 &mdash; Memory

<div class="phase-badge">Phase 2</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

<v-clicks>

- Conversation state in the current session
- Previous messages are replayed to the model

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

<v-clicks>

- Same UI
- Same model
- Still no tool use

</v-clicks>

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

<v-clicks>

- Prior turns now influence the next answer
- Follow-up questions become more coherent
- The system feels less stateless

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

<v-clicks>

- Participants can feel that state changes behavior
- Memory improves continuity before any tool is introduced
- Good moment to compare Phase 1 and Phase 2 live

</v-clicks>

</div>
</div>

<div v-click class="flow">
  <span class="flow-node">User</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM + History</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Answer</span>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Phase 3 &mdash; Tools

<div class="phase-badge badge-warm">Phase 3</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

<v-clicks>

- `search_knowledge(query)`
- Tool binding and tool execution loop

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

<v-clicks>

- Same chat UI
- Same model
- Same memory pattern

</v-clicks>

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

<v-clicks>

- The model can retrieve local knowledge before answering
- Some questions now trigger tool use
- The response loop becomes multi-step

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

<v-clicks>

- This is where the system starts to feel agent-like
- The model is no longer limited to prompt plus memory
- Good moment to switch from explanation to code inspection

</v-clicks>

</div>
</div>

<div v-click class="flow">
  <span class="flow-node">User</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-warm">Tool</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Answer</span>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Phase 4 &mdash; MCP

<div class="phase-badge badge-warm">Phase 4</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

<v-clicks>

- MCP tool exposure
- MCP discovery and invocation

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

<v-clicks>

- Same knowledge capability
- Same user-facing task
- Same general tool-augmented interaction

</v-clicks>

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

<v-clicks>

- User-facing answers may look similar
- Tool access becomes more standardized
- The integration boundary becomes cleaner

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

<v-clicks>

- Participants can separate capability from protocol
- MCP matters for architecture and interoperability
- Good final comparison point before recap and discussion

</v-clicks>

</div>
</div>

<div v-click class="flow">
  <span class="flow-node">User</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">MCP Client</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-warm">MCP Server</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Answer</span>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: center
---

## Recap

<div class="agent-formula">

`Chat -> Chat + Memory -> Chat + Tool -> Chat + Tool + MCP`

</div>

<div class="recap-grid">

<div v-click class="recap-card">
  <div class="recap-number">01</div>
  <div class="recap-title">Plain Chat</div>
  <div class="recap-desc">Response from the current prompt</div>
</div>

<div v-click class="recap-card">
  <div class="recap-number">02</div>
  <div class="recap-title">Memory</div>
  <div class="recap-desc">Response shaped by prior turns</div>
</div>

<div v-click class="recap-card">
  <div class="recap-number">03</div>
  <div class="recap-title">Tools</div>
  <div class="recap-desc">Response can use external capability</div>
</div>

<div v-click class="recap-card">
  <div class="recap-number">04</div>
  <div class="recap-title">MCP</div>
  <div class="recap-desc">Tool access becomes standardized</div>
</div>

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Discussion

<v-clicks>

- When do you actually need an **agent** instead of plain chat?
- When is a **workflow** enough without tool choice?
- Where does **MCP** help in real systems?
- What's the minimal architecture for **your** use case?

</v-clicks>

<div v-click class="discussion-cta">

**The right amount of complexity is the minimum needed for the current task.**

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>
