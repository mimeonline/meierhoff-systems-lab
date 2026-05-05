<span class="title-mark"></span>

# Multi-Agent Systems with LangGraph

Patterns verstehen. Graphen bauen. Entscheidungen explizit machen.

<p class="tagline">Ein Workshop fuer Architekturverstaendnis, saubere Implementierung und robuste Agenten-Systeme.</p>

---

## Ziel

Nach dem Workshop koennen Teilnehmende:

- typische Multi-Agent-Patterns erkennen
- Patterns in LangGraph-Strukturen uebersetzen
- kleine Graphen implementieren und ausfuehren
- Fehlerbilder frueh erkennen
- zwischen Single-Agent, Pipeline und Multi-Agent bewusst entscheiden

---

## Was sind Multi-Agenten

Ein Multi-Agent-System besteht aus mehreren spezialisierten Einheiten, die gemeinsam eine Aufgabe loesen.

- Jeder Agent hat eine begrenzte Rolle
- Kommunikation laeuft ueber State, Nachrichten oder Tool-Ergebnisse
- Koordination wird explizit modelliert
- Das Systemverhalten entsteht aus Rollen, Regeln und Ablauf

---

## Warum Multi-Agent

Multi-Agent-Architekturen helfen, wenn Aufgaben verschiedene Denkmodi brauchen.

- Trennung von Analyse, Entscheidung und Ausfuehrung
- Spezialisierte Prompts und Tools pro Rolle
- Bessere Nachvollziehbarkeit komplexer Workflows
- Kontrollierte Uebergaben zwischen Schritten
- Menschliche Kontrolle an kritischen Stellen

---

## Wann NICHT

Nicht jede Aufgabe braucht mehrere Agenten.

- Ein einfacher Chatbot reicht fuer direkte Fragen
- Eine Pipeline reicht fuer feste Prozessschritte
- Ein einzelner Agent reicht, wenn alle Tools gleich berechtigt sind
- Multi-Agenten lohnen sich erst, wenn Rollen, Grenzen oder Entscheidungen klar sind

> Erst Architekturproblem klaeren, dann Agenten einfuehren.

---

## Positive Patterns

Gute Multi-Agent-Systeme machen Architektur sichtbar.

- **Orchestrator:** zentrale Steuerung
- **Router:** explizite Pfadauswahl
- **Specialist:** getrennte Rollen
- **Blackboard:** geteilter Arbeitskontext
- **Pipeline:** kontrollierter Ablauf
- **Human:** Entscheidungspunkt fuer Menschen

---

## Pattern Tabelle

| Pattern | LangGraph-Konzept | Wofür? |
|---|---|---|
| Orchestrator | zentraler Graph | Gesamtsteuerung |
| Router | Conditional Edges | Pfadauswahl |
| Specialist | Nodes / Subgraphs | Rollentrennung |
| Blackboard | Shared State | gemeinsamer Arbeitskontext |
| Pipeline | Directed Edges | kontrollierter Ablauf |
| Human | Interrupt / Resume | menschliche Kontrolle |

---

## LangGraph Idee

LangGraph beschreibt Agenten-Workflows als Graph.

- **State** ist der explizite Kontext
- **Nodes** sind Arbeitsschritte oder Agenten
- **Edges** verbinden Schritte
- **Conditional Edges** treffen Routing-Entscheidungen
- **Interrupts** machen menschliche Eingriffe modellierbar

```python
builder = StateGraph(AgentState)
builder.add_node("analyze", analyze)
builder.add_edge(START, "analyze")
builder.add_edge("analyze", END)
graph = builder.compile()
```

---

## Mapping

Architekturpattern werden in LangGraph konkret:

- Rolle wird zu Node
- Entscheidung wird zu Conditional Edge
- Kontext wird zu State
- Ablauf wird zu Directed Edge
- Review wird zu Interrupt
- Wiederaufnahme wird zu Resume

Das Ziel ist nicht mehr Prompt-Magie, sondern eine lesbare Struktur.

---

## Orchestrator

Der Orchestrator ist die kleinste Baseline.

- Ein Graph
- Ein Node
- Eine Antwort

Gut fuer:

- Einstieg
- Vergleichspunkt
- einfache Aufgaben

---

## Router

Der Router trennt Eingaben nach Pfaden.

- Der erste Node entscheidet die Route
- Conditional Edges waehlen den naechsten Node
- Die Logik kann heuristisch oder LLM-basiert sein

Beispiel:

```text
input -> router -> math
                -> text
```

---

## Specialist

Specialists bearbeiten klar getrennte Aufgaben.

- Orchestrator entscheidet
- Math Agent loest Rechenfragen
- Text Agent formuliert oder erklaert

Der Nutzen liegt in begrenzten Rollen: nicht jeder Agent kann alles.

---

## Blackboard

Das Blackboard ist ein geteilter Arbeitskontext.

- Alle Nodes lesen denselben State
- Jeder Node schreibt sichtbare Zwischenergebnisse
- Review wird leichter, weil Kontext explizit bleibt

Gut fuer Aufgaben, bei denen mehrere Rollen denselben Arbeitsstand verbessern.

---

## Pipeline

Die Pipeline ist kein freies Agenten-Gespraech, sondern ein kontrollierter Ablauf.

```text
analyze -> process -> respond
```

Gut fuer:

- stabile Prozesse
- reproduzierbare Outputs
- klare Verantwortlichkeit pro Schritt

---

## Human

Human-in-the-loop macht Unsicherheit sichtbar.

- Das System schaetzt Confidence
- Bei niedriger Confidence wird unterbrochen
- Menschliches Feedback wird als State wieder aufgenommen

Das Pattern verhindert, dass riskante Entscheidungen nur im Prompt versteckt sind.

---

## Strands vs LangGraph

Strands und LangGraph setzen unterschiedliche Schwerpunkte.

- **Strands:** agentische App-Entwicklung mit Agent, Tools und Modell im Vordergrund
- **LangGraph:** explizite Workflow- und State-Struktur im Vordergrund
- **Strands:** gut fuer schnelle tool-nutzende Agenten
- **LangGraph:** stark fuer kontrollierte Ablaufe, Routing und Human-in-the-loop

Die Frage ist nicht welches besser ist, sondern welche Architektur sichtbar sein muss.

---

## Failure Modes

Typische Fehler entstehen, wenn Architektur unsichtbar bleibt.

- Entscheidungen stecken nur im Prompt
- State wird implizit in Nachrichten versteckt
- Agenten duerfen zu viele Tools nutzen
- Routing ist nicht validiert
- Schleifen haben kein Abbruchkriterium
- Menschen greifen zu spaet ein

---

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

---

## Workshop

Wir bauen sechs lauffaehige Phasen.

1. Orchestrator als Baseline
2. Router mit Conditional Edges
3. Specialist Agents
4. Blackboard mit Shared State
5. Pipeline mit Directed Edges
6. Human Interrupt und Resume

Jede Phase ist klein genug fuer Live Coding und vollstaendig genug fuer Diskussion.

---

## Entscheidungsmodell

Nutze die kleinste Architektur, die das Problem klar macht.

- Direkte Frage? **Single Agent**
- Fester Ablauf? **Pipeline**
- Pfadauswahl? **Router**
- Rollentrennung? **Specialists**
- Gemeinsamer Arbeitsstand? **Blackboard**
- Niedrige Sicherheit oder Risiko? **Human-in-the-loop**

Gute Agentenarchitektur beginnt mit bewusster Begrenzung.
