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
from ui.pages.datasets import render_datasets
from ui.pages.dataset_editor import render_dataset_editor
from ui.pages.dataset_info import render_dataset_info
from ui.pages.graph_builder import render_graph_builder
from ui.pages.ocr_studio import render_ocr_studio

from core.llm_service import LLMService
from connectors.factory import create_connector

DATA_PATH = "data"

st.set_page_config(layout="wide")

# =========================
# SESSION STATE
# =========================
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

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# LLM
# =========================
if st.session_state["llm"] is None:
    st.session_state["llm"] = LLMService()

# =========================
# AUTOLOAD DATASET
# =========================
if st.session_state["connector"] is None:

    if os.path.exists(DATA_PATH):

        files = sorted(os.listdir(DATA_PATH), reverse=True)

        if files:

            last_file = files[0]
            file_path = os.path.join(DATA_PATH, last_file)

            if last_file.endswith(".csv"):
                file_type = "csv"
            elif last_file.endswith(".xlsx"):
                file_type = "excel"
            else:
                file_type = None

            if file_type:

                try:
                    connector = create_connector(
                        file_type,
                        {"file_path": file_path}
                    )

                    st.session_state["connector"] = connector
                    st.session_state["file_path"] = file_path
                    st.session_state["dataset_id"] = last_file

                    st.toast(
                        f"📂 Dataset cargado automáticamente: {last_file}"
                    )

                except Exception as e:
                    st.warning(f"No se pudo cargar dataset: {e}")

# =========================
# SIDEBAR
# =========================
render_sidebar()

# =========================
# ROUTES
# =========================
ROUTES = {
    "chat": render_chat,
    "ml": render_ml,
    "charts": render_charts,
    "semantic": render_semantic,
    "data_create": render_data,
    "data_external": render_data,
    "datasets_manage": render_datasets,
    "dataset_editor": render_dataset_editor,
    "dataset_info": render_dataset_info,
    "graph_builder": render_graph_builder,
    "ranking": render_ranking,
    "recents": render_recents,
    "ocr_studio": render_ocr_studio
}

page = st.session_state.get("page", "chat")
ROUTES.get(page, render_chat)()