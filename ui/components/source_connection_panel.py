import streamlit as st

from services.source_service import SourceService


SOURCE_CONFIG = {
    "postgres": ("Connection string", "uri"),
    "mysql": ("Connection string", "uri"),
    "api": ("Base URL", "base_url"),
    "google_sheets": ("Google Sheet URL", "url"),
}


def render_source_connection_panel():

    source_type = st.selectbox(
        "Tipo de fuente",
        list(SOURCE_CONFIG.keys()),
    )

    config = {}

    label, key = SOURCE_CONFIG[source_type]

    config[key] = st.text_input(label)

    if st.button("Conectar"):

        try:

            SourceService.register(
                source_type,
                config,
            )

            st.success("✅ Fuente conectada")

        except Exception as exc:

            st.error(str(exc))