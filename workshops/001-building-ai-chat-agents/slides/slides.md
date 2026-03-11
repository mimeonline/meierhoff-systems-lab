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
<div class="meta-item">75 minutes</div>
<div class="meta-item">Five phases</div>
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
- Each phase makes one architectural change visible
- Participants compare code, behavior, and architecture after every phase

::right::

<div class="svg-container">
<svg class="phase-progress-svg" viewBox="0 0 135 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Step 1 -->
  <rect x="5" y="70" width="22" height="15" rx="3" fill="#162132" stroke="#388bd2" stroke-width="0.6"/>
  <text x="16" y="79.5" text-anchor="middle" fill="#7cc4f5" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">Chat</text>

  <!-- Step 2 -->
  <rect x="30" y="55" width="22" height="30" rx="3" fill="#162132" stroke="#388bd2" stroke-width="0.6"/>
  <text x="41" y="65" text-anchor="middle" fill="#7cc4f5" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">Memory</text>

  <!-- Step 3 -->
  <rect x="55" y="40" width="22" height="45" rx="3" fill="#162132" stroke="#e8914f" stroke-width="0.6"/>
  <text x="66" y="50" text-anchor="middle" fill="#e8914f" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">Tools</text>

  <!-- Step 4 -->
  <rect x="80" y="25" width="22" height="60" rx="3" fill="#162132" stroke="#e8914f" stroke-width="0.6"/>
  <text x="91" y="35" text-anchor="middle" fill="#e8914f" font-size="3.2" font-weight="600" font-family="Inter, sans-serif">MCP</text>

  <!-- Step 5 -->
  <rect x="105" y="12" width="22" height="73" rx="3" fill="#162132" stroke="#e8914f" stroke-width="0.6"/>
  <text x="116" y="22" text-anchor="middle" fill="#e8914f" font-size="2.8" font-weight="600" font-family="Inter, sans-serif">Compare</text>

  <!-- Gradient for arrow -->
  <defs>
    <linearGradient id="arrow-grad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#388bd2" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#7cc4f5" stop-opacity="0.6"/>
    </linearGradient>
  </defs>
  <!-- Curved arrow with offset from bars -->
  <path d="M10 64 C22 52, 32 44, 44 38 C56 30, 68 22, 80 16 C90 11, 100 7, 112 3" stroke="url(#arrow-grad)" stroke-width="0.8" stroke-linecap="round" fill="none"/>
  <!-- Arrowhead -->
  <polygon points="114,1 107,5 109,10" fill="#7cc4f5" opacity="0.5"/>
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

# The Five Phases

<p class="section-heading-sub">Each phase adds exactly one architectural change</p>

<div class="phase-pills">
  <span class="pill pill-active">Chat</span>
  <span class="pill-arrow">&rarr;</span>
  <span class="pill">Memory</span>
  <span class="pill-arrow">&rarr;</span>
  <span class="pill">Tools</span>
  <span class="pill-arrow">&rarr;</span>
  <span class="pill">MCP</span>
  <span class="pill-arrow">&rarr;</span>
  <span class="pill">Compare</span>
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

- MCP server exposes the knowledge search
- Agent loads tools via MCP adapter

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

- Same knowledge capability
- Same user-facing task
- Same agent loop pattern

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

- Answers look similar to Phase 3
- Tool access goes through a protocol boundary
- The tool is discovered, not hardcoded

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

- Capability and transport are separate concerns
- MCP matters for architecture and interoperability
- Same capability, cleaner interface boundary

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
Compare Phase 3 and Phase 4 with the same question.
The answers are similar, but the architecture is different.
-->

---

## Phase 5 &mdash; Compare

<div class="phase-badge badge-warm">Phase 5</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What was added</div>

- Both direct and MCP tools in the same agent
- User can choose which path to use

</div>
<div>

<div class="col-heading col-heading-warm">What stayed the same</div>

- Same knowledge capability
- Same agent loop
- Same chat UI

</div>
</div>

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<div class="col-heading">What behavior changed</div>

- Asking for "direct" or "MCP" uses different paths
- Asking to "compare" uses both
- Chainlit UI shows which tool name was called

</div>
<div>

<div class="col-heading col-heading-warm">Why it matters</div>

- The architectural difference becomes tangible
- Same result, different plumbing
- Participants decide when standardization is worth it

</div>
</div>

<div class="flow">
  <span class="flow-node">User</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-accent">LLM</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node flow-node-warm">Direct or MCP</span>
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

`Chat -> Memory -> Tool -> MCP -> Compare`

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
  <div class="recap-desc">Tool access via standard protocol</div>
</div>

<div class="recap-card">
  <div class="recap-number">05</div>
  <div class="recap-title">Compare</div>
  <div class="recap-desc">Direct vs MCP side by side</div>
</div>

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>

---

## Discussion

- Your company has an **FAQ system** &mdash; do you need an agent, or does RAG suffice?
- You want to **summarize emails** &mdash; plain chat, agent, or fixed workflow?
- A team builds internal **developer tools** &mdash; when does MCP help?
- What's the **minimal architecture** for your use case?
<div class="discussion-cta">

**The right amount of complexity is the minimum needed for the current task.**

</div>

<div class="brand-footer"><span class="brand-dot"></span> Meierhoff Systems Lab</div>
