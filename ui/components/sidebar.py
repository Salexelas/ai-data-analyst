import streamlit as st
import os


def render_sidebar():

    with st.sidebar:
        st.title("📊 App Data IA Analisis")

        # 🔥 DATASET ACTIVO
        if "file_path" in st.session_state and st.session_state["file_path"]:
            st.success(
                f"📊 Dataset:\n{os.path.basename(st.session_state['file_path'])}"
            )
        else:
            st.warning("No hay dataset activo")

        # =========================
        # MAIN
        # =========================
        if st.button("🆕 Nueva conversación"):
            st.session_state.page = "chat"

        st.markdown("---")

        # =========================
        # DATA
        # =========================
        with st.expander("📥 Ingresar Datos"):

            if st.button("+ Crear"):
                st.session_state.page = "data_create"

            if st.button("Fuente externa"):
                st.session_state.page = "data_external"

        # =========================
        # OCR STUDIO
        # =========================
        with st.expander("📷 OCR Studio"):

            if st.button("Procesar documentos"):
                st.session_state.page = "ocr_studio"

        # =========================
        # DATASETS
        # =========================
        with st.expander("📚 Datasets"):

            if st.button("Ver / Gestionar"):
                st.session_state.page = "datasets_manage"

        # =========================
        # GRAPH BUILDER
        # =========================
        with st.expander("🕸️ Graph Builder"):

            if st.button("Abrir canvas"):
                st.session_state.page = "graph_builder"

        # =========================
        # SEMANTIC
        # =========================
        with st.expander("🧠 Semántica"):

            if st.button("Editar"):
                st.session_state.page = "semantic"

        # =========================
        # CHARTS
        # =========================
        with st.expander("📊 Gráficos"):

            if st.button("Ver gráficos"):
                st.session_state.page = "charts"

        # =========================
        # ML
        # =========================
        with st.expander("🤖 ML"):

            if st.button("Modelos"):
                st.session_state.page = "ml"

        # =========================
        # RANKING
        # =========================
        with st.expander("🏆 Ranking"):

            if st.button("Queries"):
                st.session_state.page = "ranking"

        st.markdown("---")

        # =========================
        # RECENTS
        # =========================
        with st.expander("🕓 Recientes", expanded=True):

            queries = st.session_state.get(
                "recent_queries",
                []
            )

            for i, q in enumerate(queries):

                if st.button(
                    q,
                    key=f"sb_recent_{i}"
                ):
                    st.session_state["prefill_question"] = q
                    st.session_state.page = "chat"