import streamlit as st

from core.llm_service import LLMService


DEFAULT_STATE = {
    "llm": None,
    "page": "chat",
    "connector": None,
    "dataset_id": None,
    "file_path": None,
    "semantic_layer": None,
    "ocr_text": None,
    "ocr_df": None,
    "recent_queries": [
        "ventas por producto",
        "top clientes",
        "forecast ventas"
    ]
}


class SessionManager:

    @staticmethod
    def initialize():

        for key, value in DEFAULT_STATE.items():

            if key not in st.session_state:
                st.session_state[key] = value

        if st.session_state["llm"] is None:
            st.session_state["llm"] = LLMService()

    @staticmethod
    def get(key):

        return st.session_state.get(key)

    @staticmethod
    def set(key, value):

        st.session_state[key] = value

    @staticmethod
    def has(key):

        return key in st.session_state
    

def initialize_session():

    SessionManager.initialize()