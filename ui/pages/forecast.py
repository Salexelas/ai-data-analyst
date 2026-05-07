import streamlit as st
import os

from ui.pages.dataset_editor import (
    load_schema,
    apply_column_types
)

from ui.components.forecast.forecast_builder import (
    build_forecast_config
)

from ui.components.forecast.forecast_renderer import (
    render_forecast_chart
)


def render_forecast():

    st.title("📉 Forecast")

    connector = st.session_state.get("connector")

    if not connector:

        st.warning("Primero cargá un dataset")
        return

    file_path = st.session_state.get("file_path")

    if not file_path:

        st.warning("No hay dataset activo")
        return

    file_name = os.path.basename(file_path)

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

    config = build_forecast_config(df)

    render_forecast_chart(
        df,
        config
    )