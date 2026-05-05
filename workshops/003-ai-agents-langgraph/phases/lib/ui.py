import streamlit as st


PHASES = [
    {
        "id": "01_orchestrator",
        "label": "01 Orchestrator",
        "pattern": "Baseline",
        "description": "One graph, one node, direct answer.",
    },
    {
        "id": "02_router",
        "label": "02 Router",
        "pattern": "Conditional Edges",
        "description": "A router chooses between math and text paths.",
    },
    {
        "id": "03_specialist",
        "label": "03 Specialist",
        "pattern": "Role Separation",
        "description": "An orchestrator delegates to focused specialist nodes.",
    },
    {
        "id": "04_blackboard",
        "label": "04 Blackboard",
        "pattern": "Shared State",
        "description": "Nodes read and write a shared working context.",
    },
    {
        "id": "05_pipeline",
        "label": "05 Pipeline",
        "pattern": "Directed Edges",
        "description": "A fixed analyze, process, respond sequence.",
    },
    {
        "id": "06_human",
        "label": "06 Human",
        "pattern": "Interrupt / Resume",
        "description": "Low confidence triggers a simulated human review.",
    },
]


def apply_theme() -> None:
    st.markdown(
        """
        <style>
          :root {
            --navy: #061b2d;
            --navy-2: #0b2a42;
            --surface: #f6f8fa;
            --ink: #102233;
            --muted: #5b6a76;
            --line: #dce3e8;
            --orange: #f07a24;
            --green: #24a86b;
          }

          .stApp {
            background: linear-gradient(180deg, #eef3f6 0%, #f8fafb 38%, #ffffff 100%);
            color: var(--ink);
          }

          [data-testid="stSidebar"] {
            background: var(--navy);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
          }

          [data-testid="stSidebar"] * {
            color: #edf5fb;
          }

          [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: var(--ink);
          }

          .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
          }

          .workshop-hero {
            padding: 34px 0 30px;
            border-bottom: 1px solid var(--line);
          }

          .eyebrow {
            color: var(--orange);
            font-size: 0.82rem;
            font-weight: 760;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }

          .hero-title {
            margin: 0.25rem 0 0.6rem;
            color: var(--navy);
            font-size: clamp(2.1rem, 5vw, 4.8rem);
            font-weight: 820;
            line-height: 0.96;
            letter-spacing: 0;
          }

          .hero-copy {
            max-width: 720px;
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.6;
          }

          .phase-line {
            display: flex;
            gap: 14px;
            align-items: center;
            margin: 1.1rem 0 0.2rem;
            padding: 14px 0;
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
          }

          .phase-badge {
            display: inline-flex;
            align-items: center;
            min-height: 30px;
            padding: 4px 10px;
            border-radius: 6px;
            background: rgba(240, 122, 36, 0.12);
            color: #a8480c;
            font-size: 0.82rem;
            font-weight: 760;
          }

          .phase-summary {
            color: var(--muted);
            font-size: 0.94rem;
          }

          .result-panel {
            margin-top: 1rem;
            padding: 22px 24px;
            border-left: 5px solid var(--green);
            background: #ffffff;
            box-shadow: 0 18px 46px rgba(6, 27, 45, 0.08);
          }

          .result-panel h3 {
            margin: 0 0 10px;
            color: var(--navy);
            font-size: 1rem;
          }

          .result-panel .content {
            color: var(--ink);
            line-height: 1.58;
            white-space: pre-wrap;
          }

          .stButton > button {
            min-height: 46px;
            border: 0;
            border-radius: 6px;
            background: var(--orange);
            color: white;
            font-weight: 760;
            box-shadow: 0 10px 24px rgba(240, 122, 36, 0.22);
          }

          .stButton > button:hover {
            background: #d96518;
            color: white;
          }

          .stTextArea textarea {
            border-radius: 8px;
            border-color: var(--line);
            color: var(--ink);
            font-size: 1rem;
          }

          .stAlert {
            border-radius: 8px;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <section class="workshop-hero">
          <div class="eyebrow">LangGraph Workshop</div>
          <h1 class="hero-title">Multi-Agent Patterns</h1>
          <p class="hero-copy">
            A focused lab for understanding how orchestration, routing,
            specialists, shared state, pipelines, and human control become
            explicit LangGraph implementations.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_phase_selector() -> dict[str, str]:
    st.sidebar.markdown("## Workshop")
    st.sidebar.caption("Select a phase and run the same request through different graph patterns.")
    labels = [phase["label"] for phase in PHASES]
    selected_label = st.sidebar.selectbox("Phase", labels)
    return next(phase for phase in PHASES if phase["label"] == selected_label)


def render_phase_context(phase: dict[str, str]) -> None:
    st.markdown(
        f"""
        <div class="phase-line">
          <span class="phase-badge">{phase["pattern"]}</span>
          <span class="phase-summary">{phase["description"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input() -> str:
    return st.text_area(
        "Request",
        value="Summarize why explicit state matters in multi-agent systems.",
        height=140,
        placeholder="Ask a math or text question...",
    )


def render_output(result: str) -> None:
    st.markdown(
        f"""
        <div class="result-panel">
          <h3>Graph result</h3>
          <div class="content">{_escape_html(result)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
