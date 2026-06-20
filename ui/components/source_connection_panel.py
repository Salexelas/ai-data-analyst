import streamlit as st

from services.source_service import (
    SourceService
)


def render_source_connection_panel():

    source_type = st.selectbox(
        "Tipo de fuente",
        [
            "postgres",
            "mysql",
            "api",
            "google_sheets"
        ]
    )

    config = {}

    if source_type in (
        "postgres",
        "mysql"
    ):

        config["uri"] = st.text_input(
            "Connection string"
        )

    elif source_type == "api":

        config["base_url"] = st.text_input(
            "Base URL"
        )

    elif source_type == "google_sheets":

        config["url"] = st.text_input(
            "Google Sheet URL"
        )

    if st.button(
        "Conectar"
    ):

        try:

            SourceService.register(
                source_type,
                config
            )

            st.success(
                "✅ Fuente conectada"
            )

        except Exception as exc:

            st.error(
                str(exc)
            )