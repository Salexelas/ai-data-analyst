import streamlit as st
import plotly.express as px

from ui.components.charts.chart_filters import (
    apply_filters
)

from ui.components.charts.chart_aggregations import (
    apply_aggregation
)


def render_chart(df, config):

    if not st.button("Generar gráfico"):

        return

    try:

        # ==================================================
        # CONFIG
        # ==================================================
        chart_type = config["chart_type"]
        x_col = config["x"]
        y_col = config["y"]
        aggregation = config["aggregation"]
        group_col = config["group_by"]
        filters = config["filters"]

        # ==================================================
        # FILTERS
        # ==================================================
        df = apply_filters(
            df,
            filters
        )

        # ==================================================
        # SORT DATETIME
        # ==================================================
        if str(df[x_col].dtype).startswith("datetime"):

            df = df.sort_values(x_col)

        # ==================================================
        # AGGREGATION
        # ==================================================
        chart_df, y_axis = apply_aggregation(
            df,
            x_col,
            y_col,
            aggregation,
            group_col
        )

        # ==================================================
        # LINE
        # ==================================================
        if chart_type == "line":

            fig = px.line(
                chart_df,
                x=x_col,
                y=y_axis,
                color=None
                if group_col == "Sin grupo"
                else group_col
            )

        # ==================================================
        # SCATTER
        # ==================================================
        elif chart_type == "scatter":

            fig = px.scatter(
                chart_df,
                x=x_col,
                y=y_axis,
                color=None
                if group_col == "Sin grupo"
                else group_col
            )

        # ==================================================
        # BAR
        # ==================================================
        elif chart_type == "bar":

            fig = px.bar(
                chart_df,
                x=x_col,
                y=y_axis,
                color=None
                if group_col == "Sin grupo"
                else group_col
            )

        # ==================================================
        # PIE
        # ==================================================
        elif chart_type == "pie":

            fig = px.pie(
                chart_df,
                names=x_col,
                values=y_axis
            )

        else:

            st.error("Tipo no soportado")
            return

        # ==================================================
        # RENDER
        # ==================================================
        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==================================================
        # DATA
        # ==================================================
        with st.expander("📄 Ver datos"):

            st.dataframe(
                chart_df,
                use_container_width=True
            )

    except Exception as e:

        st.error(f"Error generando gráfico: {e}")