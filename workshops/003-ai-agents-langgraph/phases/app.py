import importlib
import sys
from pathlib import Path

import streamlit as st


WORKSHOP_ROOT = Path(__file__).resolve().parents[1]
if str(WORKSHOP_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSHOP_ROOT))

from phases.lib.ui import apply_theme, render_footer, render_header, render_input
from phases.lib.ui import render_output, render_phase_context, render_phase_details
from phases.lib.ui import render_phase_selector, render_trace


def load_phase_module(phase_id: str):
    module = importlib.import_module(f"phases.{phase_id}.graph")
    return module


def main() -> None:
    st.set_page_config(
        page_title="LangGraph Multi-Agent Workshop",
        page_icon="LG",
        layout="wide",
    )
    apply_theme()
    render_header()

    phase = render_phase_selector()
    render_phase_context(phase)

    input_col, detail_col = st.columns([1.12, 0.88], gap="large")
    with input_col:
        user_input = render_input(phase)
        run_clicked = st.button("Run graph", type="primary")

    with detail_col:
        render_phase_details(phase)

    if run_clicked:
        if not user_input.strip():
            st.warning("Enter a request before running the graph.")
            return

        with st.spinner("Running LangGraph..."):
            module = load_phase_module(phase["id"])
            if hasattr(module, "run_graph_with_trace"):
                state = module.run_graph_with_trace(user_input.strip())
                result = state["result"]
                trace = state.get("trace", [])
            else:
                result = module.run_graph(user_input.strip())
                trace = []
        render_output(result, phase)
        render_trace(trace)

    render_footer()


if __name__ == "__main__":
    main()
