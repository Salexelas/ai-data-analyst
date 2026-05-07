import streamlit as st
from agents.service import answer_question
from core.query_store import save_query

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

                if "connector" not in st.session_state:
                    st.error("Primero cargá un dataset")
                    return

                if question:
                    st.session_state.setdefault("recent_queries", [])

                    if question not in st.session_state["recent_queries"]:
                        st.session_state["recent_queries"].insert(0, question)

                    # 🔥 GUARDADO REAL (LO QUE FALTABA)
                    save_query(
                        question,
                        dataset_id=st.session_state.get("dataset_id"),
                        intent=None
                    )

                response = answer_question(
                    question=question,
                    connector=st.session_state["connector"],
                    dataset_id=st.session_state.get("dataset_id"),
                    semantic_layer=st.session_state.get("semantic_layer"),
                    llm=st.session_state["llm"]
                )

                st.session_state["last_response"] = response

        with col2:
            if st.button("Limpiar"):
                st.session_state["prefill_question"] = ""
                st.session_state.pop("last_response", None)

        st.markdown("---")

        # =========================
        # RESULTADO
        # =========================

        response = st.session_state.get("last_response")

        if response:

            if response.get("type") == "error":
                st.error(response["message"])

            elif response.get("type") == "table":

                st.subheader("📊 Resultado")
                st.dataframe(response["data"])

                if response.get("explanation"):
                    st.subheader("🧠 Insight")
                    st.write(response["explanation"])

        else:
            st.info("Todavía no ejecutaste ninguna consulta")

    # =========================
    # TABS FUTUROS
    # =========================
    with tabs[1]:
        st.markdown("### 🔀 Comparar datasets")
        st.info("Próximamente 🚧")

    with tabs[2]:
        st.markdown("### 📈 Opciones de vista")
        st.checkbox("Modo compacto")
        st.checkbox("Mostrar insight")
        st.checkbox("Mostrar SQL")