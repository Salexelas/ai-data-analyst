import streamlit as st
import os

from ui.pages.dataset_editor import (
    load_schema,
    apply_column_types
)

from ui.components.charts.chart_builder import (
    build_chart_config
)

from ui.components.charts.chart_renderer import (
    render_chart
)


def render_charts():

    st.title("📊 Constructor de gráficos")

    # ==================================================
    # VALIDATE DATASET
    # ==================================================
    connector = st.session_state.get("connector")

    if not connector:

        st.warning("Primero cargá un dataset")
        return

    # ==================================================
    # FILE PATH
    # ==================================================
    file_path = st.session_state.get("file_path")

    if not file_path:

        st.warning("No hay dataset activo")
        return

    file_name = os.path.basename(file_path)

    # ==================================================
    # LOAD DATAFRAME
    # ==================================================
    try:

        df = connector.preview(100000)

        schema = load_schema(file_name)

        df = apply_column_types(
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