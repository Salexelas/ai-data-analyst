import streamlit as st
import os


# =========================
# NAVIGATION CONFIG
# =========================
NAV = [
    {
        "section": "📥 Ingresar Datos",
        "items": [
            ("+ Crear", "data_create"),
            ("Fuente externa", "data_external"),
        ],
    },
    {
        "section": "📷 OCR Studio",
        "items": [
            ("Procesar documentos", "ocr_studio"),
        ],
    },
    {
        "section": "📚 Datasets",
        "items": [
            ("Ver / Gestionar", "datasets_manage"),
        ],
    },
    {
        "section": "🕸️ Graph Builder",
        "items": [
            ("Abrir canvas", "graph_builder"),
        ],
    },
    {
        "section": "🧠 Semántica",
        "items": [
            ("Editar", "semantic"),
        ],
    },
    {
        "section": "📊 Gráficos",
        "items": [
            ("Ver gráficos", "charts"),
        ],
    },
    {
        "section": "🤖 ML",
        "items": [
            ("Modelos", "ml"),
        ],
    },
    {
        "section": "🏆 Ranking",
        "items": [
            ("Queries", "ranking"),
        ],
    },
]


# =========================
# HELPERS
# =========================
def navigate(page: str):
    st.session_state.page = page


def render_nav_section(section):
    with st.expander(section["section"]):

        for label, page in section["items"]:

            key = f"nav_{section['section']}_{label}"

            if st.button(label, key=key):
                navigate(page)


def render_recents():
    with st.expander("🕓 Recientes", expanded=True):

        queries = st.session_state.get("recent_queries", [])

        for i, q in enumerate(queries):

            if st.button(q, key=f"sb_recent_{i}"):

                st.session_state["prefill_question"] = q
                navigate("chat")


# =========================
# MAIN SIDEBAR
# =========================
def render_sidebar():

    with st.sidebar:

        st.title("📊 App Data IA Analisis")

        # Dataset status
        if st.session_state.get("file_path"):
            st.success(
                f"📊 Dataset:\n{os.path.basename(st.session_state['file_path'])}"
            )
        else:
            st.warning("No hay dataset activo")

        # Main action
        if st.button("🆕 Nueva conversación"):
            navigate("chat")

        st.markdown("---")

        # Navigation sections (data-driven)
        for section in NAV:
            render_nav_section(section)

        st.markdown("---")

        # Recents
        render_recents()