import streamlit as st
from core.llm_service import LLMService


DEFAULT_STATE = {
    "llm": None,
    "page": "chat",
    "connector": None,
    "dataset_id": None,
    "file_path": None,
    "semantic_layer": None,
    "recent_queries": [
        "ventas por producto",
        "top clientes",
        "forecast ventas"
    ]
}


def initialize_session():

    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state["llm"] is None:
        st.session_state["llm"] = LLMService()