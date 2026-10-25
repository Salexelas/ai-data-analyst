import streamlit as st

from ui.components.charts.chart_filters import (
    render_filters
)


def build_chart_config(df):

    columns = list(df.columns)

    st.subheader("⚙️ Configuración")

    # ==================================================
    # CHART TYPE
    # ==================================================
    chart_type = st.selectbox(
        "Tipo de gráfico",
        [
            "line",
            "scatter",
            "bar",
            "pie"
        ]
    )

    # ==================================================
    # X
    # ==================================================
    x_col = st.selectbox(
        "Eje X",
        columns
    )

    # ==================================================
    # Y
    # ==================================================
    y_col = st.selectbox(
        "Eje Y",
        columns
    )

    # ==================================================
    # AGGREGATION
    # ==================================================
    aggregation = st.selectbox(
        "Agregación",
        [
            "none",
            "count",
            "sum",
            "mean",
            "min",
            "max"
        ]
    )

    # ==================================================
    # GROUP
    # ==================================================
    group_col = st.selectbox(
        "Agrupar por",
        ["Sin grupo"] + columns
    )

    # ==================================================
    # FILTERS
    # ==================================================
    filters = render_filters(df)

    # ==================================================
    # CONFIG
    # ==================================================
    return {

        "chart_type": chart_type,
        "x": x_col,
        "y": y_col,
        "aggregation": aggregation,
        "group_by": group_col,
        "filters": filters
    }