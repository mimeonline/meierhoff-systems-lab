import streamlit as st


PHASE_STATE_KEY = "selected_langgraph_phase"


PHASES = [
    {
        "id": "01_orchestrator",
        "num": "01",
        "label": "Orchestrator",
        "pattern": "Baseline",
        "description": "Ein Graph, ein Node, eine direkte Antwort als Vergleichspunkt.",
        "goal": "Baseline verstehen, bevor mehrere Rollen ins Spiel kommen.",
        "langgraph": "StateGraph mit START, assistant, END",
        "takeaway": "Nicht jede Aufgabe braucht mehrere Agenten.",
        "request": "Erkläre in drei Sätzen, warum expliziter State in Agenten-Systemen wichtig ist.",
        "flow": ["Input", "Assistant", "Result"],
        "tone": "accent",
    },
    {
        "id": "02_router",
        "num": "02",
        "label": "Router",
        "pattern": "Conditional Edges",
        "description": "Eine Entscheidung im State wählt den passenden Pfad.",
        "goal": "Routing als explizite Architekturentscheidung lesen.",
        "langgraph": "Conditional Edges mit math/text Branches",
        "takeaway": "Der Pfad ist sichtbar, nicht nur im Prompt versteckt.",
        "request": "Berechne 17 * 6 und erkläre kurz, warum diese Anfrage im Math-Pfad landet.",
        "flow": ["Input", "Router", "Math/Text", "Result"],
        "tone": "accent",
    },
    {
        "id": "03_specialist",
        "num": "03",
        "label": "Specialist",
        "pattern": "Role Separation",
        "description": "Der Orchestrator delegiert an fokussierte Specialist Nodes.",
        "goal": "Rollen trennen, ohne das System größer als nötig zu machen.",
        "langgraph": "Orchestrator Node plus Specialist Nodes",
        "takeaway": "Spezialisierung ist eine Grenze, kein Selbstzweck.",
        "request": "Formuliere diesen Satz klarer und erkläre kurz, warum dafür der Text-Specialist passt: Agenten sollten ihre Rolle kennen.",
        "flow": ["Input", "Orchestrator", "Specialist", "Result"],
        "tone": "accent",
    },
    {
        "id": "04_blackboard",
        "num": "04",
        "label": "Blackboard",
        "pattern": "Shared State",
        "description": "Alle Nodes lesen und schreiben einen gemeinsamen Arbeitskontext.",
        "goal": "Zwischenergebnisse sichtbar und überprüfbar machen.",
        "langgraph": "Shared State mit scratchpad und reviewer",
        "takeaway": "Kontext gehört in den State, nicht unsichtbar in Prompts.",
        "request": "Berechne 12 + 30 und zeige, welche Blackboard-Notizen zwischen Analyse, Specialist und Review entstehen.",
        "flow": ["Analyze", "Specialist", "Blackboard", "Review"],
        "tone": "ok",
    },
    {
        "id": "05_pipeline",
        "num": "05",
        "label": "Pipeline",
        "pattern": "Directed Edges",
        "description": "Ein fester Ablauf führt von Analyse über Verarbeitung zur Antwort.",
        "goal": "Stabile Prozesse als Alternative zu freier Agentenkoordination nutzen.",
        "langgraph": "Directed Edges: analyze -> process -> respond",
        "takeaway": "Wenn der Ablauf bekannt ist, ist Pipeline oft die sauberste Lösung.",
        "request": "Erkläre als Pipeline-Antwort, wann analyze -> process -> respond besser ist als freies Routing.",
        "flow": ["Analyze", "Process", "Respond", "Result"],
        "tone": "ok",
    },
    {
        "id": "06_human",
        "num": "06",
        "label": "Human",
        "pattern": "Interrupt / Resume",
        "description": "Niedrige Confidence unterbricht den Graphen und simuliert Review.",
        "goal": "Unsicherheit als expliziten Kontrollpunkt modellieren.",
        "langgraph": "Interrupt, MemorySaver und Command(resume=...)",
        "takeaway": "Menschliche Kontrolle wird Teil des Graphen.",
        "request": "Unsicher und kritisch: Welche Annahme soll der Assistent vor der Antwort prüfen, bevor der Human-Review fortgesetzt wird?",
        "flow": ["Assess", "Interrupt", "Human", "Resume"],
        "tone": "ok",
    },
]


_THEME_CSS = """
<style>
  :root {
    --navy: #061b2d;
    --navy-2: #0a2540;
    --navy-3: #0e3252;
    --surface: rgba(255, 255, 255, 0.04);
    --surface-2: rgba(255, 255, 255, 0.07);
    --ink: #f5f8fb;
    --muted: #9fb1c2;
    --muted-2: #6c8198;
    --orange: #ff8a2a;
    --orange-soft: #ffb479;
    --green: #3ed889;
    --line: rgba(255, 255, 255, 0.1);
    --line-strong: rgba(255, 255, 255, 0.18);
  }

  /* ── Global canvas ─────────────────────────────────────────────────── */

  .stApp {
    background:
      radial-gradient(ellipse at 85% 0%, rgba(56, 139, 210, 0.1), transparent 55%),
      radial-gradient(ellipse at 0% 100%, rgba(62, 216, 137, 0.05), transparent 55%),
      linear-gradient(180deg, var(--navy) 0%, var(--navy-2) 100%);
    color: var(--ink);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }

  .stApp [data-testid="stHeader"] {
    background: transparent;
  }

  .main .block-container {
    max-width: 1180px;
    padding-top: 2.4rem;
    padding-bottom: 4rem;
  }

  /* ── Sidebar ───────────────────────────────────────────────────────── */

  [data-testid="stSidebar"] {
    background: rgba(4, 16, 28, 0.6);
    backdrop-filter: blur(12px);
    border-right: 1px solid var(--line);
  }

  [data-testid="stSidebar"] * {
    color: var(--ink);
  }

  [data-testid="stSidebar"] h2 {
    color: var(--ink);
    font-weight: 720;
    letter-spacing: -0.02em;
    font-size: 1.15rem;
    margin-top: 1rem;
  }

  [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
  [data-testid="stSidebar"] .stCaption {
    color: var(--muted) !important;
    font-size: 0.82rem;
  }

  [data-testid="stSidebar"] label {
    color: var(--muted) !important;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .phase-nav-label {
    display: block;
    margin-top: 18px;
    margin-bottom: 8px;
    color: var(--muted);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  [data-testid="stSidebar"] .stButton {
    margin-bottom: 7px;
  }

  [data-testid="stSidebar"] .stButton > button {
    justify-content: flex-start;
    min-height: 42px;
    padding: 0 12px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.035);
    color: var(--ink);
    box-shadow: none;
    font-size: 0.86rem;
    font-weight: 650;
    letter-spacing: 0;
    transition: background 160ms ease, border-color 160ms ease, transform 160ms ease;
  }

  [data-testid="stSidebar"] .stButton > button:hover {
    transform: translateX(2px);
    background: rgba(255, 255, 255, 0.075);
    border-color: var(--line-strong);
    color: var(--ink);
    box-shadow: none;
  }

  [data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(255, 138, 42, 0.22), rgba(62, 216, 137, 0.1));
    border-color: rgba(255, 138, 42, 0.5);
    color: white;
    box-shadow: inset 3px 0 0 var(--orange);
  }

  [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, rgba(255, 138, 42, 0.28), rgba(62, 216, 137, 0.13));
    border-color: rgba(255, 138, 42, 0.62);
  }

  [data-testid="stSidebar"] .stButton > button p {
    color: inherit;
    font-size: inherit;
    font-weight: inherit;
  }

  .sidebar-note {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid var(--line);
    color: var(--muted-2);
    font-size: 0.76rem;
    line-height: 1.5;
  }

  /* ── Hero ──────────────────────────────────────────────────────────── */

  .workshop-hero {
    padding: 8px 0 28px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 1.8rem;
  }

  .title-mark {
    display: inline-block;
    width: 60px;
    height: 4px;
    margin-bottom: 18px;
    background: linear-gradient(90deg, var(--orange), var(--green));
    border-radius: 2px;
  }

  .eyebrow {
    color: var(--orange);
    font-size: 0.72rem;
    font-weight: 720;
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }

  .hero-title {
    margin: 0.4rem 0 0.8rem;
    color: var(--ink);
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.02;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, var(--ink) 0%, var(--orange-soft) 65%, var(--orange) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-copy {
    max-width: 760px;
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.6;
  }

  /* ── Phase context bar ─────────────────────────────────────────────── */

  .phase-bar {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 0 0 1.6rem;
    padding: 14px 18px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
  }

  .phase-num {
    font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    color: var(--orange);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
  }

  .phase-num.ok { color: var(--green); }

  .phase-title {
    color: var(--ink);
    font-size: 1.05rem;
    font-weight: 700;
  }

  .phase-pattern {
    margin-left: auto;
    padding: 5px 12px;
    background: rgba(255, 138, 42, 0.1);
    border: 1px solid rgba(255, 138, 42, 0.3);
    border-radius: 999px;
    color: var(--orange);
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.04em;
  }

  .phase-pattern.ok {
    background: rgba(62, 216, 137, 0.1);
    border-color: rgba(62, 216, 137, 0.3);
    color: var(--green);
  }

  .phase-desc {
    color: var(--muted);
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 0 0 1.4rem;
    max-width: 820px;
  }

  .phase-inspector {
    margin-top: 0;
    padding: 18px 20px 20px;
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.055), rgba(255, 255, 255, 0.025));
    border: 1px solid var(--line);
    border-radius: 12px;
  }

  .phase-inspector h3 {
    margin: 0 0 14px;
    color: var(--ink);
    font-size: 0.92rem;
    font-weight: 700;
    letter-spacing: 0;
  }

  .flow-map {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 18px;
  }

  .flow-node {
    min-height: 32px;
    display: inline-flex;
    align-items: center;
    padding: 6px 10px;
    border: 1px solid var(--line-strong);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.045);
    color: var(--ink);
    font-size: 0.78rem;
    font-weight: 650;
    white-space: nowrap;
  }

  .flow-node.accent {
    border-color: rgba(255, 138, 42, 0.42);
    color: var(--orange-soft);
  }

  .flow-node.ok {
    border-color: rgba(62, 216, 137, 0.36);
    color: var(--green);
  }

  .flow-arrow {
    color: var(--muted-2);
    font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.78rem;
  }

  .insight-list {
    display: grid;
    gap: 12px;
  }

  .insight-item {
    padding-top: 12px;
    border-top: 1px solid var(--line);
  }

  .insight-kicker {
    display: block;
    margin-bottom: 4px;
    color: var(--orange);
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
  }

  .insight-kicker.ok {
    color: var(--green);
  }

  .insight-text {
    color: var(--muted);
    font-size: 0.86rem;
    line-height: 1.48;
  }

  .request-note {
    margin: 0.25rem 0 0.9rem;
    padding: 12px 14px;
    color: var(--muted);
    font-size: 0.82rem;
    line-height: 1.5;
    background: rgba(255, 138, 42, 0.065);
    border: 1px solid rgba(255, 138, 42, 0.18);
    border-left: 3px solid var(--orange);
    border-radius: 8px;
  }

  .request-note strong {
    display: block;
    margin-bottom: 4px;
    color: var(--orange-soft);
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  /* ── Section labels ────────────────────────────────────────────────── */

  .section-label {
    display: block;
    color: var(--orange);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin: 0 0 0.6rem;
  }

  .section-label.ok { color: var(--green); }

  /* ── Form controls ─────────────────────────────────────────────────── */

  .stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
    font-family: Inter, ui-sans-serif, system-ui, sans-serif;
    font-size: 0.96rem !important;
    padding: 14px 16px !important;
    transition: border-color 200ms ease;
  }

  .stTextArea textarea:focus {
    border-color: rgba(255, 138, 42, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(255, 138, 42, 0.12) !important;
  }

  .stTextArea label {
    display: none !important;
  }

  .stButton > button {
    min-height: 46px;
    padding: 0 26px;
    border: 0;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--orange) 0%, #ff7a13 100%);
    color: white;
    font-weight: 700;
    font-size: 0.92rem;
    letter-spacing: 0.02em;
    box-shadow: 0 12px 28px rgba(255, 138, 42, 0.25);
    transition: transform 150ms ease, box-shadow 200ms ease;
  }

  .stButton > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(135deg, #ffa050 0%, var(--orange) 100%);
    color: white;
    box-shadow: 0 16px 36px rgba(255, 138, 42, 0.35);
  }

  .stButton > button:active {
    transform: translateY(0);
  }

  .stButton > button:focus:not(:active) {
    color: white;
    box-shadow: 0 0 0 3px rgba(255, 138, 42, 0.3);
  }

  /* ── Spinner ───────────────────────────────────────────────────────── */

  [data-testid="stSpinner"] > div {
    border-top-color: var(--orange) !important;
  }

  .stSpinner > div > div {
    color: var(--muted) !important;
  }

  /* ── Result panel ──────────────────────────────────────────────────── */

  .result-panel {
    margin-top: 1.6rem;
    padding: 24px 28px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-left: 3px solid var(--green);
    border-radius: 10px;
    box-shadow: 0 18px 46px rgba(0, 0, 0, 0.25);
  }

  .result-meta {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: -2px 0 16px;
  }

  .result-chip {
    display: inline-flex;
    align-items: center;
    min-height: 26px;
    padding: 4px 9px;
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--muted);
    font-size: 0.72rem;
    line-height: 1.2;
  }

  .result-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    color: var(--green);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  .result-head::before {
    content: "";
    width: 8px;
    height: 8px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(62, 216, 137, 0.6);
  }

  .result-content {
    color: var(--ink);
    font-size: 0.98rem;
    line-height: 1.65;
    white-space: pre-wrap;
  }

  /* ── Alerts ────────────────────────────────────────────────────────── */

  .stAlert {
    background: var(--surface) !important;
    border: 1px solid rgba(255, 138, 42, 0.3) !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
  }

  .stAlert [data-testid="stMarkdownContainer"] p {
    color: var(--ink) !important;
  }

  /* ── Footer ────────────────────────────────────────────────────────── */

  .brand-footer {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 2.6rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--line);
    color: var(--muted-2);
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }

  .brand-footer::before {
    content: "";
    width: 6px;
    height: 6px;
    background: var(--orange);
    border-radius: 50%;
  }

  /* ── Hide Streamlit chrome ─────────────────────────────────────────── */

  #MainMenu, footer, [data-testid="stToolbar"] {
    visibility: hidden;
  }

  @media (max-width: 760px) {
    .main .block-container {
      padding-top: 1.4rem;
    }

    .hero-title {
      font-size: 2.2rem;
    }

    .phase-bar {
      align-items: flex-start;
      flex-direction: column;
      gap: 7px;
    }

    .phase-pattern {
      margin-left: 0;
    }

    .phase-inspector,
    .result-panel {
      padding: 18px;
    }
  }
</style>
"""


def apply_theme() -> None:
    st.markdown(_THEME_CSS, unsafe_allow_html=True)


def render_header() -> None:
    st.markdown(
        """
        <section class="workshop-hero">
          <span class="title-mark"></span>
          <div class="eyebrow">LangGraph Workshop &middot; 003</div>
          <h1 class="hero-title">Multi-Agent Patterns</h1>
          <p class="hero-copy">
            Ein fokussiertes Lab dafür, wie Orchestrierung, Routing,
            Specialists, Shared State, Pipelines und Human Control zu
            expliziten LangGraph-Implementierungen werden.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_phase_selector() -> dict[str, str]:
    valid_phase_ids = {phase["id"] for phase in PHASES}
    selected_id = st.session_state.get(PHASE_STATE_KEY, PHASES[0]["id"])
    if selected_id not in valid_phase_ids:
        selected_id = PHASES[0]["id"]
        st.session_state[PHASE_STATE_KEY] = selected_id

    st.sidebar.markdown(
        """
        <div style="padding: 8px 0 4px;">
          <span class="title-mark" style="margin-bottom:12px;"></span>
          <h2 style="margin:0;">Workshop</h2>
          <p style="color: var(--muted); font-size: 0.82rem; margin: 6px 0 0; line-height: 1.5;">
            Sechs Phasen, sechs abgestimmte Request-Anfragen. Wähle eine Phase und prüfe das passende Pattern direkt im Graph.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown('<span class="phase-nav-label">Phasen</span>', unsafe_allow_html=True)
    for phase in PHASES:
        is_active = phase["id"] == selected_id
        clicked = st.sidebar.button(
            f"{phase['num']}  {phase['label']}",
            key=f"phase_nav_{phase['id']}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        )
        if clicked and not is_active:
            st.session_state[PHASE_STATE_KEY] = phase["id"]
            st.rerun()

    selected_phase = next(phase for phase in PHASES if phase["id"] == selected_id)
    st.sidebar.markdown(
        """
        <div class="sidebar-note">
          Jede Phase startet mit einer bewusst gewählten Anfrage, damit das jeweilige Pattern im Ergebnis sichtbar wird.
        </div>
        """,
        unsafe_allow_html=True,
    )
    return selected_phase


def render_phase_context(phase: dict[str, str]) -> None:
    tone = phase.get("tone", "accent")
    tone_class = "ok" if tone == "ok" else ""
    st.markdown(
        f"""
        <div class="phase-bar">
          <span class="phase-num {tone_class}">PHASE {phase["num"]}</span>
          <span class="phase-title">{phase["label"]}</span>
          <span class="phase-pattern {tone_class}">{phase["pattern"]}</span>
        </div>
        <p class="phase-desc">{phase["description"]}</p>
        """,
        unsafe_allow_html=True,
    )


def render_phase_details(phase: dict[str, str]) -> None:
    tone_class = "ok" if phase.get("tone") == "ok" else "accent"
    st.markdown(
        f"""
        <aside class="phase-inspector">
          <h3>Pattern Map</h3>
          {_flow_html(phase)}
          <div class="insight-list">
            <div class="insight-item">
              <span class="insight-kicker">Ziel</span>
              <div class="insight-text">{_escape_html(phase["goal"])}</div>
            </div>
            <div class="insight-item">
              <span class="insight-kicker {tone_class}">LangGraph</span>
              <div class="insight-text">{_escape_html(phase["langgraph"])}</div>
            </div>
            <div class="insight-item">
              <span class="insight-kicker">Merksatz</span>
              <div class="insight-text">{_escape_html(phase["takeaway"])}</div>
            </div>
          </div>
        </aside>
        """,
        unsafe_allow_html=True,
    )


def render_input(phase: dict[str, str]) -> str:
    st.markdown(
        f'<span class="section-label">Phase {phase["num"]} Request-Anfrage</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="request-note"><strong>Abgestimmt auf {phase["label"]}</strong>Die vorbereitete Anfrage steht im Eingabefeld und kann direkt ausgeführt oder angepasst werden.</p>',
        unsafe_allow_html=True,
    )
    return st.text_area(
        f"Phase {phase['num']} Request-Anfrage",
        value=phase["request"],
        height=140,
        placeholder="Ask a math or text question...",
        key=f"request_{phase['id']}",
        label_visibility="collapsed",
    )


def render_output(result: str, phase: dict[str, str]) -> None:
    st.markdown(
        f"""
        <div class="result-panel">
          <div class="result-head">Graph Result</div>
          <div class="result-meta">
            <span class="result-chip">{phase["num"]} {phase["label"]}</span>
            <span class="result-chip">{phase["pattern"]}</span>
          </div>
          <div class="result-content">{_escape_html(result)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        '<div class="brand-footer">Meierhoff Systems Lab</div>',
        unsafe_allow_html=True,
    )


def _flow_html(phase: dict[str, str]) -> str:
    nodes = []
    last_index = len(phase["flow"]) - 1
    for index, label in enumerate(phase["flow"]):
        if index > 0:
            nodes.append('<span class="flow-arrow">-&gt;</span>')
        tone = " ok" if index == last_index and phase.get("tone") == "ok" else ""
        if index == 1:
            tone = " accent"
        nodes.append(f'<span class="flow-node{tone}">{_escape_html(label)}</span>')
    return f'<div class="flow-map">{"".join(nodes)}</div>'


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
