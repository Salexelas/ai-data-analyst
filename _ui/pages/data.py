import streamlit as st

from ui.components.file_upload_panel import (
    render_file_upload_panel
)

from ui.components.ocr_panel import (
    render_ocr_panel
)

from ui.components.source_connection_panel import (
    render_source_connection_panel
)

from ui.components.preview_panel import (
    render_preview_panel
)


def render_data():

    st.title("📥 Gestión de Datos")

    upload_tab, connection_tab, preview_tab = st.tabs(
        [
            "📂 Subir archivo",
            "🔗 Conectar fuente",
            "📊 Preview"
        ]
    )

    with upload_tab:

        render_file_upload_panel()

        st.markdown("---")

        render_ocr_panel()

    with connection_tab:

        render_source_connection_panel()

    with preview_tab:

        render_preview_panel()