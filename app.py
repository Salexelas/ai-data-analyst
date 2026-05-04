import streamlit as st

from ui.components.sidebar import render_sidebar
from ui.pages.chat import render_chat
from ui.pages.ml import render_ml
from ui.pages.charts import render_charts
from ui.pages.semantic import render_semantic
from ui.pages.data import render_data
from ui.pages.ranking import render_ranking
from ui.pages.recents import render_recents
from core.llm_service import LLMService

st.set_page_config(layout="wide")

# =========================
# 🔹 STATE GLOBAL
# =========================
if "llm" not in st.session_state:
    st.session_state["llm"] = LLMService()

if "page" not in st.session_state:
    st.session_state.page = "chat"

# 👉 NUEVO (estado compartido)
if "recent_queries" not in st.session_state:
    st.session_state.recent_queries = [
        "ventas por producto",
        "top clientes",
        "forecast ventas"
    ]

# =========================
# 🔹 SIDEBAR
# =========================
render_sidebar()

# =========================
# 🔥 ROUTER
# =========================
ROUTES = {
    "chat": render_chat,
    "ml": render_ml,
    "charts": render_charts,
    "semantic": render_semantic,
    "data_create": render_data,
    "data_external": render_data,
    "ranking": render_ranking,
    "recents": render_recents
}

# =========================
# ▶️ EXECUTE PAGE
# =========================
ROUTES.get(st.session_state.page, render_chat)()