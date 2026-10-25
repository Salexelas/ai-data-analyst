import streamlit as st
import os

from dataset_editor.services.schema_service import SchemaService
from dataset_editor.services.type_service import TypeService

from ui.components.charts.chart_builder import (
    build_chart_config
)

from ui.components.charts.chart_renderer import (
    render_chart
)


def render_charts():

    st.title("📊 Constructor de gráficos")

    # ==================================================
    # VALIDATE CONNECTOR
    # ==================================================
    connector = st.session_state.get("connector")

    if not connector:
        st.warning("Primero cargá un dataset")
        return

    # ==================================================
    # VALIDATE FILE
    # ==================================================
    file_path = st.session_state.get("file_path")

    if not file_path:
        st.warning("No hay dataset activo")
        return

    file_name = os.path.basename(file_path)

    # ==================================================
    # LOAD DATA
    # ==================================================
    try:

        df = connector.preview(100000)

        schema = SchemaService.load(file_name)

        df = TypeService.apply(
            df,
            schema
        )

    except Exception as e:

        st.error(f"Error cargando dataset: {e}")
        return

    # ==================================================
    # CONFIG
    # ==================================================
    config = build_chart_config(df)

    # ==================================================
    # RENDER
    # ==================================================
    render_chart(
        df,
        config
    )