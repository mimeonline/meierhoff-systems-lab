<!-- .slide: class="cover" -->

<span class="title-mark"></span>
<span class="kicker">Workshop 003</span>

# Multi-Agent Systems<br/>mit LangGraph

<p class="tagline">Patterns verstehen. Graphen bauen. Entscheidungen explizit machen.</p>

<div class="cover-meta">
  <span class="pill accent">6 Phasen</span>
  <span class="pill">Live Coding</span>
  <span class="pill ok">LangGraph</span>
</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">01 — Einleitung</div>

# Warum dieser Workshop

<p class="section-sub">Wenn Aufgaben komplex werden, gehört die Struktur in den Graphen, nicht nur in den Prompt.</p>

---

<div class="chapter-badge">Einleitung</div>

## Ziel

Nach dem Workshop können Teilnehmende:

- typische **Multi-Agent-Patterns** erkennen
- Patterns in **LangGraph-Strukturen** übersetzen
- kleine Graphen implementieren und ausführen
- **Fehlerbilder** früh erkennen
- zwischen Single-Agent, Pipeline und Multi-Agent bewusst entscheiden

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Einleitung</div>

## Was sind Multi-Agenten

Ein Multi-Agent-System besteht aus mehreren spezialisierten Einheiten, die gemeinsam eine Aufgabe lösen.

- Jeder Agent hat eine **begrenzte Rolle**
- Kommunikation läuft über **expliziten State** und klar definierte Übergaben
- Koordination wird **explizit** modelliert
- Das Systemverhalten entsteht aus Rollen, Regeln und Ablauf

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Einleitung</div>

## Warum Multi-Agent

Multi-Agent-Architekturen helfen, wenn Aufgaben verschiedene Denkmodi brauchen.

<div class="cols-2">
<div>
<span class="col-label">Vorteile</span>

- Trennung von Analyse, Entscheidung, Ausführung
- Spezialisierte Prompts und Tools pro Rolle
- Bessere Nachvollziehbarkeit komplexer Workflows

</div>
<div>
<span class="col-label green">Konsequenz</span>

- Kontrollierte Übergaben zwischen Schritten
- Menschliche Kontrolle an kritischen Stellen
- Fehler werden lokalisierbar

</div>
</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Einleitung</div>

## Wann NICHT

Nicht jede Aufgabe braucht mehrere Agenten.

- Ein einfacher **Chatbot** reicht für direkte Fragen
- Eine **Pipeline** reicht für feste Prozessschritte
- Ein **einzelner Agent** reicht, wenn alle Tools gleich berechtigt sind
- Multi-Agenten lohnen sich erst, wenn Rollen, Grenzen oder Entscheidungen klar sind

> Erst Architekturproblem klären, dann Agenten einführen.

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">02 — Patterns</div>

# Sechs Patterns, ein Graph

<p class="section-sub">Architektur gehört in den Graphen, nicht in versteckte Prompt-Regeln.</p>

---

<div class="chapter-badge">Patterns</div>

## Positive Patterns

<div class="cards">
  <div class="card"><span class="card-num">01</span><span class="card-title">Orchestrator</span><span class="card-desc">Wer hält den Ablauf zusammen?</span></div>
  <div class="card"><span class="card-num">02</span><span class="card-title">Router</span><span class="card-desc">Welcher Pfad ist als nächstes dran?</span></div>
  <div class="card"><span class="card-num">03</span><span class="card-title">Specialist</span><span class="card-desc">Wer bearbeitet welche Rolle?</span></div>
  <div class="card green"><span class="card-num">04</span><span class="card-title">Blackboard</span><span class="card-desc">Wo liegt der gemeinsame Arbeitsstand?</span></div>
  <div class="card green"><span class="card-num">05</span><span class="card-title">Pipeline</span><span class="card-desc">Welche Reihenfolge ist fest?</span></div>
  <div class="card green"><span class="card-num">06</span><span class="card-title">Human</span><span class="card-desc">Wo muss ein Mensch eingreifen?</span></div>
</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Patterns</div>

## Pattern Tabelle

| Pattern | LangGraph-Konzept | Wofür? |
|---|---|---|
| Orchestrator | zentraler Graph | Wer hält den Ablauf zusammen? |
| Router | Conditional Edges | Welcher Pfad ist als nächstes dran? |
| Specialist | Nodes / Subgraphs | Wer bearbeitet welche Rolle? |
| Blackboard | Shared State | Wo liegt der gemeinsame Arbeitsstand? |
| Pipeline | Directed Edges | Welche Reihenfolge ist fest? |
| Human | Interrupt / Resume | Wo muss ein Mensch eingreifen? |

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">03 — LangGraph</div>

# Vom Pattern zum Graphen

<p class="section-sub">State, Nodes, Edges &mdash; und sonst nichts.</p>

---

<div class="chapter-badge">LangGraph</div>

## LangGraph Idee

LangGraph beschreibt Agenten-Workflows als Graph.

<dl class="defs">
  <dt>State</dt><dd>der explizite, geteilte Kontext</dd>
  <dt>Nodes</dt><dd>Arbeitsschritte oder Agenten</dd>
  <dt>Edges</dt><dd>Verbindung zwischen Schritten</dd>
  <dt>Conditional Edges</dt><dd>Routing-Entscheidungen</dd>
  <dt>Interrupts</dt><dd>menschliche Eingriffe</dd>
</dl>

```python
builder = StateGraph(AgentState)
builder.add_node("analyze", analyze)
builder.add_edge(START, "analyze")
builder.add_edge("analyze", END)
graph = builder.compile()
```

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">LangGraph</div>

## Maturity & Einsetzbarkeit

LangGraph ist kein Randexperiment mehr, aber trotzdem Infrastruktur, die bewusst betrieben werden muss.

<div class="cards four">
  <div class="card"><span class="card-num">GitHub</span><span class="card-title">31k+ Stars</span><span class="card-desc">5k+ Forks, viele Releases, aktive Community.</span></div>
  <div class="card"><span class="card-num">PyPI</span><span class="card-title">45M+ Downloads / Monat</span><span class="card-desc">Breite Nutzung im Python-Ökosystem.</span></div>
  <div class="card green"><span class="card-num">Status</span><span class="card-title">Production / Stable</span><span class="card-desc">PyPI classifier, Python 3.10 bis 3.13.</span></div>
  <div class="card green"><span class="card-num">Industrie</span><span class="card-title">Klarna, Replit, Elastic</span><span class="card-desc">Offiziell genannte Nutzungssignale.</span></div>
</div>

<div class="callout warn">Einsetzbar für Produktion, wenn Observability, Version Pinning, Security Updates und klare State-Grenzen mitgedacht werden.</div>

<p class="source-note">Stand: Mai 2026 · Quellen: GitHub, PyPI Stats, PyPI Project Metadata</p>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">LangGraph</div>

## Mapping

Architekturpattern werden in LangGraph konkret.

<div class="cols-2">
<div>
<span class="col-label">Architektur</span>

- Rolle
- Entscheidung
- Kontext
- Ablauf
- Review
- Wiederaufnahme

</div>
<div>
<span class="col-label green">LangGraph</span>

- **Node**
- **Conditional Edge**
- **State**
- **Directed Edge**
- **Interrupt**
- **Resume**

</div>
</div>

<div class="callout">Das Ziel ist nicht mehr Prompt-Magie, sondern eine <strong>lesbare Struktur</strong>.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">04 — Phasen</div>

# Sechs Phasen Live Coding

<p class="section-sub">Klein genug für Code, vollständig genug für Diskussion.</p>

---

<div class="chapter-badge">Phase 1</div>

## Orchestrator

Der Orchestrator hält den Ablauf zusammen. In Phase 1 bleibt er bewusst minimal.

<div class="flow">
  <span class="flow-node">Input</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node accent">Orchestrator</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Output</span>
</div>

<div class="cols-2">
<div>
<span class="col-label">Bestandteile</span>

- Ein Graph
- Ein Node
- Eine Antwort

</div>
<div>
<span class="col-label green">Gut für</span>

- Einstieg
- Vergleichspunkt
- einfache Aufgaben

</div>
</div>

<div class="callout warn">Orchestrator ist die Gesamtsteuerung. Routing, Specialists, Blackboard und Human Review können Teil dieser Steuerung sein.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 2</div>

## Router

Der Router beantwortet eine engere Frage: Welcher Pfad ist als nächstes dran?

<div class="flow">
  <span class="flow-node">Input</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node accent">Router</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Math</span>
  <span class="flow-arrow">/</span>
  <span class="flow-node ok">Text</span>
</div>

- Der erste Node entscheidet die **Route**
- **Conditional Edges** wählen den nächsten Node
- Die Logik kann **heuristisch** oder **LLM-basiert** sein

```python
builder.add_conditional_edges("router", choose_route, {"math": "math_agent", "text": "text_agent"})
```

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 3</div>

## Specialist

Specialists beantworten: Wer bearbeitet welche Rolle?

<div class="flow compact">
  <span class="flow-node accent">Orchestrator</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Brief</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Math</span>
  <span class="flow-arrow">/</span>
  <span class="flow-node ok">Text</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node accent">Review</span>
</div>

- **Orchestrator** erstellt einen Auftrag
- Specialist arbeitet auf `delegation_brief`
- Review baut das finale Ergebnis zusammen

```python
state["delegation_brief"] -> specialist -> state["specialist_result"]
```

<div class="callout warn">Der Unterschied zum Router: Nicht nur der Pfad ist explizit, sondern auch der Auftrag an die Rolle.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 4</div>

## Blackboard

Das Blackboard beantwortet: Wo liegt der gemeinsame Arbeitsstand?

<div class="flow compact">
  <span class="flow-node accent">analyze writes</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node ok">blackboard</span>
  <span class="flow-arrow">&larr;</span>
  <span class="flow-node">specialist updates</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node accent">reviewer reads</span>
</div>

- `blackboard` ist ein gemeinsames **State-Dict**
- jeder Node liest und schreibt denselben Arbeitsstand
- das Ergebnis enthält einen sichtbaren **Snapshot**

```python
blackboard.update({"draft": answer, "specialist": "math_agent"})
```

<div class="callout">Der Unterschied zum Specialist: Nicht ein Auftrag wird übergeben, sondern ein gemeinsamer Arbeitsstand wächst.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 5</div>

## Pipeline

Die Pipeline beantwortet: Welche Reihenfolge ist fest?

<div class="flow">
  <span class="flow-node accent">analyze</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node accent">process</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node ok">respond</span>
</div>

<div class="cols-2">
<div>
<span class="col-label">Eigenschaften</span>

- stabile Prozesse
- reproduzierbare Outputs

</div>
<div>
<span class="col-label green">Konsequenz</span>

- klare Verantwortlichkeit pro Schritt
- testbar und versionierbar

</div>
</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge green">Phase 6</div>

## Human in the Loop

Human-in-the-loop beantwortet: Wo muss ein Mensch eingreifen?

<div class="flow compact">
  <span class="flow-node accent">assess</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">low confidence?</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node ok">interrupt</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">resume</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node accent">respond</span>
</div>

- Das System schätzt **Confidence**
- bei niedriger Confidence stoppt der Graph **vor der Antwort**
- Menschliches Feedback wird als **State** wieder aufgenommen

```python
feedback = interrupt({"intervention_point": "before respond", "question": human_question})
graph.invoke(Command(resume=feedback), config=config)
```

<div class="callout">Der wichtige Punkt ist nicht nur Review, sondern <strong>wo</strong> der Mensch eingreifen muss.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">05 — Vergleich</div>

# Strands oder LangGraph?

<p class="section-sub">Eine Frage: Was muss sichtbar sein?</p>

---

<div class="chapter-badge">Vergleich</div>

## Strands vs LangGraph

<div class="cols-2">
<div>
<span class="col-label">Strands</span>

- agentische App-Entwicklung
- Agent, Tools, Modell im Vordergrund
- gut für schnelle, tool-nutzende Agenten

</div>
<div>
<span class="col-label green">LangGraph</span>

- explizite Workflow- und State-Struktur
- Routing und Human-in-the-loop
- stark für kontrollierte Abläufe

</div>
</div>

<div class="callout">Entscheidend ist: Was reicht als Tool-Agent, und was braucht <strong>explizite Kontrolle im Graphen</strong>?</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Vergleich</div>

## Pattern Mapping

Strands benennt Ausführungsformen. LangGraph modelliert die Architekturbausteine darunter.

| Strands Pattern | Kontrollidee | LangGraph-Pattern im Workshop |
|---|---|---|
| Agent-as-Tool | Orchestrator LLM wählt Sub-Agent | Orchestrator + Specialist |
| Workflow | Developer-defined DAG | Pipeline |
| Graph | Developer Edges + LLM Routing | Router + Conditional Edges |
| Swarm | Agenten übergeben autonom | Human / Blackboard nur mit klaren Grenzen |

<div class="callout">In LangGraph entscheiden wir bewusst, welche Kontrolle explizit im Graphen liegt: Route, Rolle, State, Ablauf oder Review.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Vergleich</div>

## Pattern-Fragen

Die Patterns sind am klarsten, wenn jedes eine andere Frage beantwortet.

<div class="decision">
  <div class="q">Orchestrator</div><div class="a"><span class="accent">Wer hält den Ablauf zusammen?</span></div>
  <div class="q">Router</div>      <div class="a"><span class="accent">Welcher Pfad ist als nächstes dran?</span></div>
  <div class="q">Specialist</div>  <div class="a"><span class="ok">Wer bearbeitet welche Rolle?</span></div>
  <div class="q">Blackboard</div>  <div class="a"><span class="ok">Wo liegt der gemeinsame Arbeitsstand?</span></div>
  <div class="q">Pipeline</div>    <div class="a"><span class="ok">Welche Reihenfolge ist fest?</span></div>
  <div class="q">Human</div>       <div class="a"><span class="ok">Wo muss ein Mensch eingreifen?</span></div>
</div>

<div class="callout warn">Orchestrator ist die übergreifende Steuerung. Die anderen Patterns machen einzelne Steuerungsfragen explizit.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">06 — Fallen</div>

# Wo es kippt

<p class="section-sub">Typische Fehler, wenn Architektur unsichtbar bleibt.</p>

---

<div class="chapter-badge">Fallen</div>

## Failure Modes

Typische Fehler entstehen, wenn Architektur unsichtbar bleibt.

- Entscheidungen stecken nur im **Prompt**
- State wird **implizit** in Nachrichten versteckt
- Agenten dürfen **zu viele Tools** nutzen
- Routing ist **nicht validiert**
- Schleifen haben **kein Abbruchkriterium**
- Menschen greifen **zu spät** ein

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Fallen</div>

## Anti-Patterns

| Anti-Pattern | Symptom | Gegenmittel in LangGraph |
|---|---|---|
| Over-Agentification | mehrere Agenten für einfache Aufgabe | erst Single-Agent / Pipeline prüfen |
| Hidden State | Kontext liegt unsichtbar in Prompts | expliziter Shared State |
| Unbounded Loop | Agenten laufen endlos weiter | Recursion Limit / Exit Criteria |
| Tool Explosion | jeder Agent kann alles | Tools pro Rolle begrenzen |
| God Orchestrator | zentrale Steuerung wird zu komplex | Subgraphs / klarere Zuständigkeiten |
| Hallucinated Routing | falscher Pfad wird gewählt | explizite Router-Regeln + Validierung |
| Prompt-Coupled Architecture | Architektur steckt nur im Prompt | Graphstruktur explizit modellieren |

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">07 — Entscheidung</div>

# Wann was?

<p class="section-sub">Die kleinste Architektur, die das Problem klar macht.</p>

---

<div class="chapter-badge green">Entscheidung</div>

## Entscheidungsmodell

<div class="decision">
  <div class="q">Direkte Frage?</div>           <div class="a"><span class="accent">Single Agent</span></div>
  <div class="q">Ablauf zusammenhalten?</div>   <div class="a"><span class="accent">Orchestrator</span></div>
  <div class="q">Feste Reihenfolge?</div>       <div class="a"><span class="accent">Pipeline</span></div>
  <div class="q">Nächster Pfad?</div>           <div class="a"><span class="accent">Router</span></div>
  <div class="q">Rollenverantwortung?</div>     <div class="a"><span class="ok">Specialists</span></div>
  <div class="q">Gemeinsamer Arbeitsstand?</div><div class="a"><span class="ok">Blackboard</span></div>
  <div class="q">Menschlicher Eingriff?</div>   <div class="a"><span class="ok">Human-in-the-loop</span></div>
</div>

<div class="callout">Gute Agentenarchitektur beginnt mit <strong>bewusster Begrenzung</strong>.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">08 — Workshop</div>

# Jetzt bauen wir

<p class="section-sub">Sechs lauffähige Phasen, ein durchgängiger Graph.</p>

---

<div class="chapter-badge green">Workshop</div>

## Sechs Phasen

<div class="cards">
  <div class="card"><span class="card-num">01</span><span class="card-title">Orchestrator</span><span class="card-desc">Ablauf zusammenhalten.</span></div>
  <div class="card"><span class="card-num">02</span><span class="card-title">Router</span><span class="card-desc">Nächsten Pfad wählen.</span></div>
  <div class="card"><span class="card-num">03</span><span class="card-title">Specialist</span><span class="card-desc">Rolle bearbeiten.</span></div>
  <div class="card green"><span class="card-num">04</span><span class="card-title">Blackboard</span><span class="card-desc">Arbeitsstand teilen.</span></div>
  <div class="card green"><span class="card-num">05</span><span class="card-title">Pipeline</span><span class="card-desc">Reihenfolge festlegen.</span></div>
  <div class="card green"><span class="card-num">06</span><span class="card-title">Human</span><span class="card-desc">Eingriffspunkt setzen.</span></div>
</div>

<div class="callout">Jede Phase ist klein genug für Live Coding und vollständig genug für Diskussion.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge green">Ende</div>

# Vielen Dank

<div class="thanks-layout closing">
  <div class="thanks-copy">
    <span class="col-label">Kontakt</span>
    <span class="thanks-name">Michael Meierhoff</span>
    <span class="thanks-brand">Meierhoff Systems Lab</span>
    <span class="thanks-links">
      <a href="https://www.linkedin.com/in/michael-meierhoff-b5426458/">LinkedIn</a>
      <a href="https://github.com/mimeonline/meierhoff-systems-lab">Workshop Repo</a>
    </span>
  </div>

  <div>
    <span class="col-label green">Ressourcen</span>
    <div class="cards two thanks-resource-cards">
      <div class="card green"><span class="card-num">Docs</span><span class="card-title">LangGraph</span><span class="card-desc"><a href="https://langchain-ai.github.io/langgraph/">Documentation</a></span></div>
      <div class="card green"><span class="card-num">Code</span><span class="card-title">LangGraph</span><span class="card-desc"><a href="https://github.com/langchain-ai/langgraph">GitHub Repo</a></span></div>
      <div class="card"><span class="card-num">Vergleich</span><span class="card-title">Strands Agents</span><span class="card-desc"><a href="https://strandsagents.com/">Website</a></span></div>
      <div class="card"><span class="card-num">UI</span><span class="card-title">Streamlit</span><span class="card-desc"><a href="https://streamlit.io/">Website</a></span></div>
    </div>
  </div>
</div>

<div class="brand">Meierhoff Systems Lab</div>
