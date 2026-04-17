import streamlit as st
from core.llm_service import LLMService
from ui.ui_source import render_source_selector
from ui.ui_semantic import render_semantic_ui
from ui.ui_query import render_query_ui

st.set_page_config(page_title="AI Data Analyst", layout="wide")

if "llm" not in st.session_state:
    st.session_state["llm"] = LLMService()

st.title("🔥 AI Data Analyst")
st.write("Conectá tu fuente de datos en segundos")

render_source_selector()

if "connector" in st.session_state:

    connector = st.session_state["connector"]

    st.subheader("📚 Schema")
    st.dataframe(connector.get_schema())

    st.subheader("👀 Preview")
    preview = connector.preview()
    st.dataframe(preview)

    # 👇 SOLO ESTO
    render_semantic_ui(connector)

    render_query_ui()