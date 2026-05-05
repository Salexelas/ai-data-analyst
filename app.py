import streamlit as st
import os

from ui.components.sidebar import render_sidebar
from ui.pages.chat import render_chat
from ui.pages.ml import render_ml
from ui.pages.charts import render_charts
from ui.pages.semantic import render_semantic
from ui.pages.data import render_data
from ui.pages.ranking import render_ranking
from ui.pages.recents import render_recents
from core.llm_service import LLMService
from connectors.factory import create_connector
from ui.pages.datasets import render_datasets

st.set_page_config(layout="wide")

DATA_PATH = "data"

# =========================
# 🔹 STATE GLOBAL
# =========================
if "llm" not in st.session_state:
    st.session_state["llm"] = LLMService()

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "recent_queries" not in st.session_state:
    st.session_state.recent_queries = [
        "ventas por producto",
        "top clientes",
        "forecast ventas"
    ]

# =========================
# 🔥 AUTOLOAD DATASET
# =========================
if "connector" not in st.session_state:

    if os.path.exists(DATA_PATH):

        files = sorted(os.listdir(DATA_PATH), reverse=True)

        if files:
            last_file = files[0]
            file_path = os.path.join(DATA_PATH, last_file)

            file_type = "csv" if last_file.endswith(".csv") else "excel"

            try:
                connector = create_connector(file_type, {"file_path": file_path})

                st.session_state["connector"] = connector
                st.session_state["file_path"] = file_path

                st.toast(f"📂 Dataset cargado automáticamente: {last_file}")

            except Exception as e:
                st.warning(f"No se pudo cargar dataset: {e}")

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
    "datasets_manage": render_datasets,
    "ranking": render_ranking,
    "recents": render_recents
}

# =========================
# ▶️ EXECUTE PAGE
# =========================
ROUTES.get(st.session_state.page, render_chat)()