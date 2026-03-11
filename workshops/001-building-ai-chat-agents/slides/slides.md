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

```mermaid {theme: 'base', scale: 0.7}
flowchart LR
  U[User] --> LLM
  LLM --> D{Tool?}
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

<div class="col-heading">What changed</div>

<v-clicks>

- Baseline Chainlit chat and one model call
- No memory, no tools, one response step
- This is the **reference point** for every later comparison

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What to notice</div>

<v-clicks>

- Each turn stands alone
- Follow-up questions **lose context**
- Ask: *"now summarize that in one sentence"*

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

<div class="col-heading">What changed</div>

<v-clicks>

- Conversation state in the current session
- Same UI, same model, still no tool use
- Prior turns now **influence** the next answer

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What to notice</div>

<v-clicks>

- Follow-up questions become **coherent**
- The chat feels less stateless
- State changes behavior even before new capabilities

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

<div class="col-heading">What changed</div>

<v-clicks>

- `search_knowledge(query)` plus tool binding
- Same chat UI, same model, same memory
- The model can **retrieve local knowledge** before answering

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What to notice</div>

<v-clicks>

- Some questions **trigger tool use**
- The response loop is now **multi-step**
- The system is no longer "just chatting"

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

<div class="col-heading">What changed</div>

<v-clicks>

- MCP tool exposure, discovery, and invocation
- Same knowledge capability, same user-facing task
- Tool access becomes **standardized** and extensible

</v-clicks>

</div>
<div>

<div class="col-heading col-heading-warm">What to notice</div>

<v-clicks>

- User-facing behavior may look **similar**
- The integration boundary is **cleaner**
- Architecture improves even when capability stays the same

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
