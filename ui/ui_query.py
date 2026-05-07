import streamlit as st
from agents.service import answer_question
from core.query_store import save_query

def render_query_ui():

    st.subheader("💬 Pregunta")

    question = st.text_input("Escribí tu pregunta")

    if st.button("Ejecutar"):

        if not question:
            st.warning("Escribí una pregunta")
            return

        # 🔥 guardar SIEMPRE
        save_query(
            question,
            dataset_id=st.session_state.get("dataset_id"),
            intent=None  # después podés conectar con tu intent detector
        )

        response = answer_question(
            question,
            st.session_state["connector"],
            st.session_state.get("dataset_id"),
            st.session_state.get("semantic_layer"),
            st.session_state["llm"]
        )

        # 🔹 ERROR
        if response.get("type") == "error":
            st.error(response["message"])
            return

        # 🔹 DATA
        if response.get("type") == "table":
            st.subheader("📊 Resultado")
            st.dataframe(response["data"], use_container_width=True)

        # 🔹 INSIGHT
        if response.get("explanation") is not None:
            st.subheader("🧠 Insight")
            st.write(response["explanation"])