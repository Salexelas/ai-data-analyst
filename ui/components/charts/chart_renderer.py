import streamlit as st
import plotly.express as px

from ui.components.charts.chart_aggregations import apply_aggregation
from ui.components.charts.chart_filters import apply_filters


CHART_BUILDERS = {
    "line": px.line,
    "scatter": px.scatter,
    "bar": px.bar,
}


def unpack_config(config):
    return (
        config["chart_type"],
        config["x"],
        config["y"],
        config["aggregation"],
        config["group_by"],
        config["filters"],
    )


def prepare_chart_data(
    df,
    x_col,
    y_col,
    aggregation,
    group_col,
    filters,
):
    df = apply_filters(df, filters)

    if str(df[x_col].dtype).startswith("datetime"):
        df = df.sort_values(x_col)

    return apply_aggregation(
        df,
        x_col,
        y_col,
        aggregation,
        group_col,
    )


def build_chart(
    chart_type,
    chart_df,
    x_col,
    y_axis,
    group_col,
):
    if chart_type == "pie":
        return px.pie(
            chart_df,
            names=x_col,
            values=y_axis,
        )

    builder = CHART_BUILDERS.get(chart_type)

    if builder is None:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    color = None if group_col == "Sin grupo" else group_col

    return builder(
        chart_df,
        x=x_col,
        y=y_axis,
        color=color,
    )


def render_chart_output(fig, chart_df):
    st.plotly_chart(
        fig,
        width="stretch",
    )

    with st.expander("📄 Ver datos"):
        st.dataframe(
            chart_df,
            width="stretch",
        )


def render_chart(df, config):
    if not st.button("Generar gráfico"):
        return

    try:
        (
            chart_type,
            x_col,
            y_col,
            aggregation,
            group_col,
            filters,
        ) = unpack_config(config)

        chart_df, y_axis = prepare_chart_data(
            df,
            x_col,
            y_col,
            aggregation,
            group_col,
            filters,
        )

        fig = build_chart(
            chart_type,
            chart_df,
            x_col,
            y_axis,
            group_col,
        )

        render_chart_output(
            fig,
            chart_df,
        )

    except Exception as exc:
        st.error(f"Error generating chart: {exc}")