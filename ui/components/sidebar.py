import streamlit as st

def render_sidebar():

    with st.sidebar:
        st.title("📊 App Data IA Analisis")

            # 🔥 DATASET ACTIVO (SIEMPRE VISIBLE)
        if "file_path" in st.session_state:
            import os
            st.success(f"📊 Dataset:\n{os.path.basename(st.session_state['file_path'])}")
        else:
            st.warning("No hay dataset activo")

        if st.button("🆕 Nueva conversación"):
            st.session_state.page = "chat"

        st.markdown("---")

        with st.expander("📥 Ingresar Datos"):
            if st.button("+ Crear"):
                st.session_state.page = "data_create"
        
            if st.button("Fuente externa"):
                st.session_state.page = "data_external"

        with st.expander("📚 Datasets"):
            if st.button("Ver / Gestionar"):
                st.session_state.page = "datasets_manage"

        with st.expander("🧠 Semántica"):
            if st.button("Editar"):
                st.session_state.page = "semantic"

        with st.expander("📊 Gráficos"):
            if st.button("Ver gráficos"):
                st.session_state.page = "charts"

        with st.expander("🤖 ML"):
            if st.button("Modelos"):
                st.session_state.page = "ml"

        with st.expander("🏆 Ranking"):
            if st.button("Queries"):
                st.session_state.page = "ranking"

        st.markdown("---")

        # 🔥 RECENTS DINÁMICO
        with st.expander("🕓 Recientes", expanded=True):

            queries = st.session_state.get("recent_queries", [])

            for i, q in enumerate(queries):
                if st.button(q, key=f"sb_recent_{i}"):
                    st.session_state.page = "recents"