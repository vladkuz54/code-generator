from datetime import datetime
from typing import Any, Dict, List, Tuple

import streamlit as st

from graph.graph import app

st.set_page_config(page_title="Code Generator", layout="wide")


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Describe your coding task and I will generate a solution. "
                    "Node-by-node responses are shown on the right panel."
                ),
            }
        ]

    if "runs" not in st.session_state:
        st.session_state.runs = []


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

            .stApp {
                font-family: 'Space Grotesk', sans-serif;
                color: #eaf2ff;
                background: radial-gradient(circle at 15% 15%, #1f2b52 0%, #141c35 32%, #0c1224 65%, #060a14 100%);
            }

            h1, h2, h3 {
                color: #f4f8ff;
                letter-spacing: 0.02em;
            }

            p, span, label, div {
                color: #d9e5ff;
            }

            .hero {
                background: linear-gradient(135deg, rgba(58, 91, 179, 0.45), rgba(34, 173, 193, 0.24));
                border: 1px solid rgba(137, 168, 255, 0.28);
                border-radius: 18px;
                padding: 14px 16px;
                margin-bottom: 14px;
                box-shadow: 0 10px 26px rgba(0, 0, 0, 0.35);
            }

            .card {
                border: 1px solid rgba(150, 181, 255, 0.24);
                border-radius: 14px;
                background: rgba(17, 27, 52, 0.82);
                padding: 10px 12px;
                margin-bottom: 10px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.28);
            }

            .meta {
                font-size: 0.83rem;
                color: #8fb7ff;
                font-family: 'IBM Plex Mono', monospace;
            }

            .stCodeBlock {
                border: 1px solid rgba(139, 166, 255, 0.2);
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def stringify(value: Any) -> str:
    if value is None:
        return "None"
    return str(value)


def run_graph_with_debug(query: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    node_events: List[Dict[str, Any]] = []
    final_state: Dict[str, Any] = {}

    for event in app.stream({"query": query}, stream_mode="updates"):
        for node_name, payload in event.items():
            payload = payload or {}
            final_state.update(payload)
            node_events.append(
                {
                    "node": node_name,
                    "payload": payload,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
            )

    return final_state, node_events


def render_node_window() -> None:
    st.subheader("Node responses")

    if not st.session_state.runs:
        st.info("Run the first request to see architect/coder/tester outputs.")
        return

    for run_index, run in enumerate(reversed(st.session_state.runs), start=1):
        title = f"Run {len(st.session_state.runs) - run_index + 1}: {run['query'][:60]}"
        with st.expander(title, expanded=(run_index == 1)):
            st.markdown(f"<div class='meta'>Time: {run['time']}</div>", unsafe_allow_html=True)

            for idx, event in enumerate(run["events"], start=1):
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(
                    (
                        f"**Step {idx} | Node: {event['node']}**  "
                        f"<span class='meta'>{event['timestamp']}</span>"
                    ),
                    unsafe_allow_html=True,
                )

                payload: Dict[str, Any] = event["payload"]
                if not payload:
                    st.code("No payload", language="text")
                else:
                    for key, value in payload.items():
                        st.caption(key)
                        st.code(stringify(value), language="text")
                st.markdown("</div>", unsafe_allow_html=True)


def build_assistant_answer(final_state: Dict[str, Any]) -> str:
    coder_output = stringify(final_state.get("coder_output"))
    return coder_output


init_session_state()
inject_styles()

st.markdown(
    """
    <div class="hero">
        <h2 style="margin:0;">Code Generator Chat</h2>
        <p style="margin:6px 0 0 0;">
            Left: dialogue with the assistant. Right: every response returned by each graph node.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Session")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Graph runs", len(st.session_state.runs))

    if st.button("Clear history", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Describe your coding task and I will generate a solution. "
                    "Node-by-node responses are shown on the right panel."
                ),
            }
        ]
        st.session_state.runs = []
        st.rerun()

chat_col, debug_col = st.columns([2, 1], gap="large")

with chat_col:
    st.subheader("Chat")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Write a coding task...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Running graph..."):
                final_state, node_events = run_graph_with_debug(user_query)
                assistant_reply = build_assistant_answer(final_state)
            st.markdown(assistant_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )
        st.session_state.runs.append(
            {
                "query": user_query,
                "events": node_events,
                "final_state": final_state,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        st.rerun()

with debug_col:
    render_node_window()

    