import streamlit as st
from agents.router import route_question

def render_query_ui():

    st.subheader("💬 Pregunta")
    question = st.text_input("Escribí tu pregunta")

    if st.button("Ejecutar"):
        response = route_question(
            question,
            st.session_state["connector"],
            st.session_state.get("semantic_layer"),
            st.session_state.get("dataset_id")
        )

        # 🔹 SQL (debug opcional)
        if response.get("sql"):
            st.subheader("🧠 SQL generado")
            st.code(response["sql"], language="sql")

        # 🔹 TABLE
        if response["type"] == "table":
            st.subheader("📊 Resultado")
            st.dataframe(response["data"])

        # 🔹 EXPLANATION
        if response.get("explanation"):
            st.subheader("🧠 Insight")
            st.write(response["explanation"])

        # 🔹 ERROR
        elif response["type"] == "error":
            st.error(response["message"])

        # 🔹 TEXT (por si agregás después)
        elif response["type"] == "text":
            st.write(response["message"])