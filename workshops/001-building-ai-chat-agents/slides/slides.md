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
<div class="meta-item">60 minutes</div>
<div class="meta-item">Four phases</div>
<div class="meta-item">Local knowledge search</div>
</div>

<p class="cover-footer">Meierhoff Systems Lab</p>

</div>

---
transition: fade-out
layout: two-cols
layoutClass: gap-8
---

## Why This Workshop Exists

- LLM chat is often labeled an **"agent"** too early
- The useful question is: **what changed in the system?**
- This workshop adds one capability at a time
- We alternate between short explanation and live coding
- Participants compare code, behavior, and architecture after every phase

::right::

<div class="svg-container">
<svg class="phase-progress-svg" viewBox="0 0 110 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Step 1 -->
  <rect x="5" y="70" width="22" height="15" rx="3" fill="#162132" stroke="#388bd2" stroke-width="0.6"/>
  <text x="16" y="79.5" text-anchor="middle" fill="#7cc4f5" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">Chat</text>

  <!-- Step 2 -->
  <rect x="30" y="52" width="22" height="33" rx="3" fill="#162132" stroke="#388bd2" stroke-width="0.6"/>
  <text x="41" y="62" text-anchor="middle" fill="#7cc4f5" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">Memory</text>

  <!-- Step 3 -->
  <rect x="55" y="35" width="22" height="50" rx="3" fill="#162132" stroke="#e8914f" stroke-width="0.6"/>
  <text x="66" y="45" text-anchor="middle" fill="#e8914f" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">Tools</text>

  <!-- Step 4 -->
  <rect x="80" y="17" width="22" height="68" rx="3" fill="#162132" stroke="#e8914f" stroke-width="0.6"/>
  <text x="91" y="27" text-anchor="middle" fill="#e8914f" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">MCP</text>

  <!-- Arrow line -->
  <path d="M16 69 C30 58, 48 45, 64 33 S84 18, 92 12" stroke="#388bd2" stroke-width="0.7" stroke-dasharray="2.5 2" stroke-linecap="round" fill="none" opacity="0.45"/>
  <polygon points="96,9 89,12 93,18" fill="#388bd2" opacity="0.45"/>
</svg>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---
layout: two-cols
layoutClass: gap-8
---

## What Is An AI Agent?

- A model alone is **not** the whole system
- Memory can preserve conversational state
- Tools extend capability beyond generation
- The key shift is a **loop**: decide, act, observe, respond
<div class="agent-formula">

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

<div class="phase-pills">
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

- Baseline Chainlit chat
- One model call per user message

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

- No memory
- No tools
- One response step only

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

- None yet
- This is plain chat only
- Each turn stands alone

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

- This is the reference point for the workshop
- It shows what plain chat can and cannot do
- The limitations are visible immediately

</div>
</div>

<div class="flow">
  <span class="flow-node">User</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Answer</span>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

<!--
After this slide, switch into the first live-coding step.
Use a simple follow-up question to make the missing context visible.
-->

---

## Phase 2 &mdash; Memory

<div class="phase-badge">Phase 2</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

- Conversation state in the current session
- Previous messages are replayed to the model

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

- Same UI
- Same model
- Still no tool use

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

- Prior turns now influence the next answer
- Follow-up questions become more coherent
- The system feels less stateless

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

- Participants can feel that state changes behavior
- Memory improves continuity before any tool is introduced
- It separates statefulness from tool use

</div>
</div>

<div class="flow">
  <span class="flow-node">User</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM + History</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Answer</span>
</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

<!--
Compare Phase 1 and Phase 2 with the same follow-up prompt.
Stress that memory changes continuity, not capability.
-->

---

## Phase 3 &mdash; Tools

<div class="phase-badge badge-warm">Phase 3</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

- `search_knowledge(query)`
- Tool binding and tool execution loop

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

- Same chat UI
- Same model
- Same memory pattern

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

- The model can retrieve local knowledge before answering
- Some questions now trigger tool use
- The response loop becomes multi-step

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

- This is where the system starts to feel agent-like
- The model is no longer limited to prompt plus memory
- Tool use changes both behavior and architecture

</div>
</div>

<div class="flow">
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

<!--
Switch here from explanation to code inspection.
Show where the tool is registered and where the loop executes it.
-->

---

## Phase 4 &mdash; MCP

<div class="phase-badge badge-warm">Phase 4</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

- MCP tool exposure
- MCP discovery and invocation

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

- Same knowledge capability
- Same user-facing task
- Same general tool-augmented interaction

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

- User-facing answers may look similar
- Tool access becomes more standardized
- The integration boundary becomes cleaner

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

- Participants can separate capability from protocol
- MCP matters for architecture and interoperability
- The same capability can be exposed through a cleaner interface boundary

</div>
</div>

<div class="flow">
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

<!--
Use this phase to distinguish capability from integration pattern.
The behavior may look similar, but the architecture is different.
-->

---
layout: center
---

## Recap

<div class="agent-formula">

`Chat -> Chat + Memory -> Chat + Tool -> Chat + Tool + MCP`

</div>

<div class="recap-grid">

<div class="recap-card">
  <div class="recap-number">01</div>
  <div class="recap-title">Plain Chat</div>
  <div class="recap-desc">Response from the current prompt</div>
</div>

<div class="recap-card">
  <div class="recap-number">02</div>
  <div class="recap-title">Memory</div>
  <div class="recap-desc">Response shaped by prior turns</div>
</div>

<div class="recap-card">
  <div class="recap-number">03</div>
  <div class="recap-title">Tools</div>
  <div class="recap-desc">Response can use external capability</div>
</div>

<div class="recap-card">
  <div class="recap-number">04</div>
  <div class="recap-title">MCP</div>
  <div class="recap-desc">Tool access becomes standardized</div>
</div>

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Discussion

- When do you actually need an **agent** instead of plain chat?
- When is a **workflow** enough without tool choice?
- Where does **MCP** help in real systems?
- What's the minimal architecture for **your** use case?
<div class="discussion-cta">

**The right amount of complexity is the minimum needed for the current task.**

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>
