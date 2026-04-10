import streamlit as st
from connectors.factory import create_connector
from semantic.utils import get_dataset_id, load_semantic_layer

def render_source_selector():
    source_type = st.selectbox(
        "Seleccioná tipo de fuente",
        ["duckdb", "postgres", "mysql", "excel", "csv", "google_sheets", "api"]
    )

    config = {}

    if source_type == "duckdb":
        use_demo = st.checkbox("Usar tabla demo", value=True)

        uploaded_file = None
        if not use_demo:
            uploaded_file = st.file_uploader("Subí CSV/Parquet", type=["csv", "parquet"])

        if uploaded_file:
            config["file"] = uploaded_file
        elif use_demo:
            config["file"] = None

    elif source_type in ["postgres", "mysql"]:
        use_demo = st.checkbox("Usar demo", value=True)

        if use_demo:
            config["uri"] = None
        else:
            default_uri = (
                "postgresql://user:pass@localhost:5432/db"
                if source_type == "postgres"
                else "mysql+pymysql://user:pass@localhost:3306/db"
            )
            config["uri"] = st.text_input("Connection String", default_uri)

    elif source_type == "google_sheets":
        config["url"] = st.text_input("Google Sheet URL")

    elif source_type == "api":
        config["base_url"] = st.text_input("Base URL", "https://api.example.com")

    elif source_type in ["excel", "csv"]:
        uploaded_file = st.file_uploader("📂 Subí archivo", type=["csv", "xlsx"])

        if uploaded_file:
            config["file"] = uploaded_file

    if st.button("🚀 Conectar"):
        connector = create_connector(source_type, config)

        st.session_state["connector"] = connector
        dataset_id = get_dataset_id(source_type, config)
        st.session_state["dataset_id"] = dataset_id

        loaded = load_semantic_layer(dataset_id)
        if loaded:
            st.session_state["semantic_layer"] = loaded
            st.info("📂 Capa semántica cargada")

        st.success("✅ Conectado")