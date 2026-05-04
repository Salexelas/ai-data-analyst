import streamlit as st

def render_semantic():

    st.title("🧠 Capa Semántica")

    tabs = st.tabs([
        "🔤 Aliases",
        "📊 Métricas",
        "🧪 Test"
    ])

    # -------------------------
    # 🔤 ALIASES
    # -------------------------
    with tabs[0]:
        st.text_input("Columna")
        st.text_input("Alias")
        st.button("Agregar alias")

    # -------------------------
    # 📊 METRICS
    # -------------------------
    with tabs[1]:
        st.text_input("Nombre métrica")
        st.text_input("SQL")
        st.button("Agregar métrica")

    # -------------------------
    # 🧪 TEST
    # -------------------------
    with tabs[2]:
        st.text_input("Consulta de prueba")
        st.button("Testear")
        st.info("Resultado de test")