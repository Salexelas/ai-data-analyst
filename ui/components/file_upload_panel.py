import streamlit as st

from core.session_manager import (
    SessionManager
)

from ui.services.dataset_service import (
    DatasetService
)

from services.source_service import (
    SourceService
)


def render_file_upload_panel():

    st.subheader(
        "📂 Subir Dataset"
    )

    uploaded_file = st.file_uploader(
        "Subir CSV / Excel",
        type=["csv", "xlsx"]
    )

    if not uploaded_file:
        return

    if st.button(
        "Cargar archivo"
    ):

        file_path = (
            DatasetService
            .save_uploaded_file(
                uploaded_file
            )
        )

        file_type = (
            "csv"
            if uploaded_file.name.endswith(
                ".csv"
            )
            else "excel"
        )

        SourceService.register(
            file_type,
            {
                "file_path": file_path
            }
        )

        SessionManager.set(
            "file_path",
            file_path
        )

        st.success(
            f"✅ Dataset guardado en {file_path}"
        )