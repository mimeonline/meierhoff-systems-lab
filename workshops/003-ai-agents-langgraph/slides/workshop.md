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

<p class="section-sub">Architektur sichtbar machen, bevor Prompts komplex werden.</p>

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
- Kommunikation läuft über **State, Nachrichten oder Tool-Ergebnisse**
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

<p class="section-sub">Architektur sichtbar machen statt im Prompt verstecken.</p>

---

<div class="chapter-badge">Patterns</div>

## Positive Patterns

<div class="cards">
  <div class="card"><span class="card-num">01</span><span class="card-title">Orchestrator</span><span class="card-desc">Zentrale Steuerung. Eine Quelle der Wahrheit für den Ablauf.</span></div>
  <div class="card"><span class="card-num">02</span><span class="card-title">Router</span><span class="card-desc">Explizite Pfadauswahl an Verzweigungen.</span></div>
  <div class="card"><span class="card-num">03</span><span class="card-title">Specialist</span><span class="card-desc">Getrennte Rollen mit klaren Grenzen.</span></div>
  <div class="card green"><span class="card-num">04</span><span class="card-title">Blackboard</span><span class="card-desc">Geteilter Arbeitskontext für alle Nodes.</span></div>
  <div class="card green"><span class="card-num">05</span><span class="card-title">Pipeline</span><span class="card-desc">Kontrollierter, reproduzierbarer Ablauf.</span></div>
  <div class="card green"><span class="card-num">06</span><span class="card-title">Human</span><span class="card-desc">Entscheidungspunkt für Menschen im Loop.</span></div>
</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Patterns</div>

## Pattern Tabelle

| Pattern | LangGraph-Konzept | Wofür? |
|---|---|---|
| Orchestrator | zentraler Graph | Gesamtsteuerung |
| Router | Conditional Edges | Pfadauswahl |
| Specialist | Nodes / Subgraphs | Rollentrennung |
| Blackboard | Shared State | gemeinsamer Arbeitskontext |
| Pipeline | Directed Edges | kontrollierter Ablauf |
| Human | Interrupt / Resume | menschliche Kontrolle |

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

Der Orchestrator ist die kleinste Baseline.

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

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 2</div>

## Router

Der Router trennt Eingaben nach Pfaden.

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

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 3</div>

## Specialist

Specialists bearbeiten klar getrennte Aufgaben.

<div class="flow">
  <span class="flow-node accent">Orchestrator</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Math Agent</span>
  <span class="flow-arrow">/</span>
  <span class="flow-node ok">Text Agent</span>
</div>

- **Orchestrator** entscheidet
- **Math Agent** löst Rechenfragen
- **Text Agent** formuliert oder erklärt

<div class="callout warn">Der Nutzen liegt in <strong>begrenzten Rollen</strong> &mdash; nicht jeder Agent kann alles.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 4</div>

## Blackboard

Das Blackboard ist ein geteilter Arbeitskontext.

- Alle Nodes lesen denselben **State**
- Jeder Node schreibt **sichtbare Zwischenergebnisse**
- Review wird leichter, weil Kontext **explizit** bleibt

<div class="callout">Gut für Aufgaben, bei denen mehrere Rollen denselben Arbeitsstand verbessern.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<div class="chapter-badge">Phase 5</div>

## Pipeline

Die Pipeline ist kein freies Agenten-Gespräch, sondern ein kontrollierter Ablauf.

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

Human-in-the-loop macht Unsicherheit sichtbar.

<div class="flow">
  <span class="flow-node accent">Agent</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Confidence?</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node ok">Human Review</span>
  <span class="flow-arrow">&rarr;</span>
  <span class="flow-node">Resume</span>
</div>

- Das System schätzt **Confidence**
- Bei niedriger Confidence wird **unterbrochen**
- Menschliches Feedback wird als **State** wieder aufgenommen

<div class="callout">Das Pattern verhindert, dass riskante Entscheidungen nur im Prompt versteckt sind.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">05 — Vergleich</div>

# Strands oder LangGraph?

<p class="section-sub">Zwei Schwerpunkte, eine Frage: was muss sichtbar sein?</p>

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

<div class="callout">Die Frage ist nicht, welches besser ist, sondern <strong>welche Architektur sichtbar sein muss</strong>.</div>

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

| Anti-Pattern | Symptom | Gegenmittel |
|---|---|---|
| Over-Agentification | mehrere Agenten für einfache Aufgabe | erst Single-Agent / Pipeline prüfen |
| Hidden State | Kontext liegt unsichtbar in Prompts | expliziter Shared State |
| Unbounded Loop | Agenten laufen endlos weiter | Recursion Limit / Exit Criteria |
| Tool Explosion | jeder Agent kann alles | Tools pro Rolle begrenzen |
| God Orchestrator | zentrale Steuerung wird zu komplex | Subgraphs / klare Zuständigkeit |
| Hallucinated Routing | falscher Pfad wird gewählt | explizite Router-Regeln |
| Prompt-Coupled Architecture | Architektur steckt nur im Prompt | Graphstruktur explizit |

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">07 — Workshop</div>

# Jetzt bauen wir

<p class="section-sub">Sechs lauffähige Phasen, ein durchgängiger Graph.</p>

---

<div class="chapter-badge green">Workshop</div>

## Sechs Phasen

<div class="cards">
  <div class="card"><span class="card-num">01</span><span class="card-title">Orchestrator</span><span class="card-desc">Baseline mit einem Node.</span></div>
  <div class="card"><span class="card-num">02</span><span class="card-title">Router</span><span class="card-desc">Conditional Edges.</span></div>
  <div class="card"><span class="card-num">03</span><span class="card-title">Specialist</span><span class="card-desc">Spezialisierte Agents.</span></div>
  <div class="card green"><span class="card-num">04</span><span class="card-title">Blackboard</span><span class="card-desc">Shared State.</span></div>
  <div class="card green"><span class="card-num">05</span><span class="card-title">Pipeline</span><span class="card-desc">Directed Edges.</span></div>
  <div class="card green"><span class="card-num">06</span><span class="card-title">Human</span><span class="card-desc">Interrupt &amp; Resume.</span></div>
</div>

<div class="callout">Jede Phase ist klein genug für Live Coding und vollständig genug für Diskussion.</div>

<div class="brand">Meierhoff Systems Lab</div>

---

<!-- .slide: class="section" -->

<div class="section-num">08 — Entscheidung</div>

# Wann was?

<p class="section-sub">Die kleinste Architektur, die das Problem klar macht.</p>

---

<div class="chapter-badge green">Entscheidung</div>

## Entscheidungsmodell

<div class="decision">
  <div class="q">Direkte Frage?</div>           <div class="a"><span class="accent">Single Agent</span></div>
  <div class="q">Fester Ablauf?</div>           <div class="a"><span class="accent">Pipeline</span></div>
  <div class="q">Pfadauswahl?</div>             <div class="a"><span class="accent">Router</span></div>
  <div class="q">Rollentrennung?</div>          <div class="a"><span class="ok">Specialists</span></div>
  <div class="q">Gemeinsamer Arbeitsstand?</div><div class="a"><span class="ok">Blackboard</span></div>
  <div class="q">Niedrige Sicherheit?</div>     <div class="a"><span class="ok">Human-in-the-loop</span></div>
</div>

<div class="callout">Gute Agentenarchitektur beginnt mit <strong>bewusster Begrenzung</strong>.</div>

<div class="brand">Meierhoff Systems Lab</div>
