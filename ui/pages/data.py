import streamlit as st

def render_data():

    st.title("📥 Gestión de Datos")

    tabs = st.tabs([
        "📂 Subir archivo",
        "🔗 Conectar fuente",
        "📊 Preview"
    ])

    # -------------------------
    # 📂 UPLOAD
    # -------------------------
    with tabs[0]:
        st.file_uploader("Subir CSV / Excel")
        st.button("Cargar archivo")

    # -------------------------
    # 🔗 CONNECT
    # -------------------------
    with tabs[1]:
        st.selectbox("Tipo de fuente", ["Postgres", "MySQL", "API", "Google Sheets"])
        st.text_input("Connection string / URL")
        st.button("Conectar")

    # -------------------------
    # 📊 PREVIEW
    # -------------------------
    with tabs[2]:
        st.info("Vista previa del dataset")
        st.dataframe([])