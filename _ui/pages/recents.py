import streamlit as st


def _render_queries(queries, delete=False):

    for i, q in enumerate(queries):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(q)

        with col2:

            if delete:

                if st.button(
                    "❌",
                    key=f"rec_delete_{i}"
                ):
                    st.session_state.recent_queries.pop(i)
                    st.rerun()

            elif st.button(
                "Abrir",
                key=f"rec_open_{i}"
            ):
                st.session_state.page = "chat"
                st.session_state.prefill_question = q


def render_recents():

    st.title("🕓 Conversaciones recientes")

    tabs = st.tabs([
        "📜 Historial",
        "⭐ Favoritas",
        "🧹 Gestión"
    ])

    queries = st.session_state.get(
        "recent_queries",
        []
    )

    # =========================
    # 📜 HISTORIAL
    # =========================

    with tabs[0]:

        st.subheader("Últimas consultas")

        if not queries:
            st.info("No hay consultas todavía")
        else:
            _render_queries(queries)

    # =========================
    # ⭐ FAVORITAS
    # =========================

    with tabs[1]:

        st.subheader("Consultas guardadas")
        st.info("No hay favoritas todavía")

    # =========================
    # 🧹 GESTIÓN
    # =========================

    with tabs[2]:

        st.subheader("Administrar historial")

        if st.button(
            "🗑️ Borrar historial completo"
        ):
            st.session_state.recent_queries = []
            st.success("Historial eliminado")

        st.markdown("---")

        _render_queries(
            queries,
            delete=True
        )