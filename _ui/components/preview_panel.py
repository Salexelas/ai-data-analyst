import streamlit as st

from core.session_manager import (
    SessionManager
)


def render_preview_panel():

    dataset_id = SessionManager.get(
        "dataset_id"
    )

    file_path = SessionManager.get(
        "file_path"
    )

    st.subheader(
        "📊 Dataset activo"
    )

    if not dataset_id:

        st.info(
            "No hay dataset cargado."
        )

        return

    st.write(
        f"Dataset: {dataset_id}"
    )

    if file_path:

        st.write(
            f"Archivo: {file_path}"
        )