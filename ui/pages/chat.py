import streamlit as st

def render_chat():

    st.title("💬 Nueva conversación")

    tabs = st.tabs(["💬 Chat", "🔀 Comparación", "📈 Vista"])

    # =========================
    # TAB CHAT
    # =========================
    with tabs[0]:

        default_q = st.session_state.get("prefill_question", "")

        question = st.text_input(
            "Escribí tu pregunta...",
            value=default_q
        )

        col1, col2 = st.columns([1,1])

        with col1:
            if st.button("Ejecutar"):

                # 🔥 GUARDAR EN RECENTS
                if question:
                    if question not in st.session_state.recent_queries:
                        st.session_state.recent_queries.insert(0, question)

                st.success("Ejecutado (UI mock)")

        with col2:
            if st.button("Limpiar"):
                st.session_state.prefill_question = ""

        st.markdown("---")

        st.subheader("📊 Resultado")
        st.info("Acá se muestra la tabla")

        st.subheader("🧠 Insight")
        st.info("Acá se muestra el análisis")

    # =========================
    # TAB COMPARACIÓN
    # =========================
    with tabs[1]:
        st.markdown("### 🔀 Comparar datasets")

        col1, col2 = st.columns(2)

        with col1:
            st.selectbox("Tabla A", ["ventas", "clientes"])

        with col2:
            st.selectbox("Tabla B", ["ventas", "clientes"])

        st.button("Comparar")

    # =========================
    # TAB VISTA
    # =========================
    with tabs[2]:
        st.markdown("### 📈 Opciones de vista")

        st.checkbox("Modo compacto")
        st.checkbox("Mostrar insight")
        st.checkbox("Mostrar SQL")