import streamlit as st
from connectors.factory import create_connector
from semantic.utils import get_dataset_id, load_semantic_layer

def render_data():

    st.title("📥 Gestión de Datos")

    tabs = st.tabs([
        "📂 Subir archivo",
        "🔗 Conectar fuente",
        "📊 Preview"
    ])

    # -------------------------
    # 📂 UPLOAD (CSV / Excel)
    # -------------------------
    with tabs[0]:

        file = st.file_uploader("Subir CSV / Excel", type=["csv", "xlsx"])

        if file and st.button("Cargar archivo"):

            # detectar tipo simple
            file_type = "csv" if file.name.endswith(".csv") else "excel"

            connector = create_connector(file_type, {"file": file})

            st.session_state["connector"] = connector

            dataset_id = get_dataset_id(file_type, {"file": file.name})
            st.session_state["dataset_id"] = dataset_id

            loaded = load_semantic_layer(dataset_id)
            if loaded:
                st.session_state["semantic_layer"] = loaded

            st.success("✅ Dataset cargado")

    # -------------------------
    # 🔗 CONNECT (DB / API)
    # -------------------------
    with tabs[1]:

        source_type = st.selectbox(
            "Tipo de fuente",
            ["postgres", "mysql", "api", "google_sheets"]
        )

        config = {}

        if source_type in ["postgres", "mysql"]:
            config["uri"] = st.text_input("Connection string")

        elif source_type == "api":
            config["base_url"] = st.text_input("Base URL")

        elif source_type == "google_sheets":
            config["url"] = st.text_input("Google Sheet URL")

        if st.button("Conectar"):

            connector = create_connector(source_type, config)

            st.session_state["connector"] = connector

            dataset_id = get_dataset_id(source_type, config)
            st.session_state["dataset_id"] = dataset_id

            loaded = load_semantic_layer(dataset_id)
            if loaded:
                st.session_state["semantic_layer"] = loaded

            st.success("✅ Conectado")

    # -------------------------
    # 📊 PREVIEW
    # -------------------------
    with tabs[2]:

        if "connector" in st.session_state:

            st.info("Vista previa del dataset")

            preview = st.session_state["connector"].preview()
            st.dataframe(preview)

        else:
            st.warning("Primero cargá una fuente de datos")