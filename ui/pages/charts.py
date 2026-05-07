import streamlit as st
import os
import plotly.express as px
import pandas as pd

from ui.pages.dataset_editor import (
    load_schema,
    apply_column_types
)


def render_charts():

    st.title("📊 Visualización")

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
    # COLUMNS
    # ==================================================
    columns = list(df.columns)

    # ==================================================
    # TABS
    # ==================================================
    tabs = st.tabs([
        "📈 Línea / Dispersión",
        "📊 Barras",
        "🥧 Torta",
        "📉 Forecast"
    ])

    # ==================================================
    # 📈 LINE / SCATTER
    # ==================================================
    with tabs[0]:

        st.subheader("📈 Configuración")

        # ==================================================
        # CHART TYPE
        # ==================================================
        chart_type = st.selectbox(
            "Tipo de gráfico",
            [
                "line",
                "scatter"
            ],
            key="chart_type"
        )

        # ==================================================
        # X
        # ==================================================
        x_col = st.selectbox(
            "Eje X",
            columns,
            key="line_x"
        )

        # ==================================================
        # Y
        # ==================================================
        y_col = st.selectbox(
            "Eje Y",
            columns,
            key="line_y"
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
            ],
            key="aggregation"
        )

        # ==================================================
        # GROUP BY
        # ==================================================
        group_col = st.selectbox(
            "Agrupar por",
            ["Sin grupo"] + columns,
            key="group_col"
        )

        # ==================================================
        # FILTERS
        # ==================================================
        st.subheader("🎯 Filtros")

        filter_col = st.selectbox(
            "Filtrar por",
            ["Sin filtro"] + columns,
            key="filter_col"
        )

        filtered_df = df.copy()

        if filter_col != "Sin filtro":

            unique_values = (
                filtered_df[filter_col]
                .dropna()
                .unique()
                .tolist()
            )

            selected_values = st.multiselect(
                "Valores",
                unique_values,
                default=unique_values[:5]
                if len(unique_values) > 5
                else unique_values,
                key="filter_values"
            )

            if selected_values:

                filtered_df = filtered_df[
                    filtered_df[filter_col]
                    .isin(selected_values)
                ]

        # ==================================================
        # GENERATE CHART
        # ==================================================
        if st.button(
            "Generar gráfico",
            key="btn_line_chart"
        ):

            try:

                chart_df = filtered_df.copy()

                # ==================================================
                # SORT DATETIME
                # ==================================================
                if str(chart_df[x_col].dtype).startswith("datetime"):

                    chart_df = chart_df.sort_values(x_col)

                # ==================================================
                # AGGREGATIONS
                # ==================================================
                if aggregation != "none":

                    # ==================================================
                    # COUNT
                    # ==================================================
                    if aggregation == "count":

                        # -------------------------
                        # WITH GROUP
                        # -------------------------
                        if group_col != "Sin grupo":

                            chart_df = (
                                chart_df
                                .groupby([x_col, group_col])
                                .size()
                                .reset_index(name="count")
                            )

                            y_axis = "count"

                        # -------------------------
                        # WITHOUT GROUP
                        # -------------------------
                        else:

                            chart_df = (
                                chart_df
                                .groupby(x_col)
                                .size()
                                .reset_index(name="count")
                            )

                            y_axis = "count"

                    # ==================================================
                    # OTHER AGGREGATIONS
                    # ==================================================
                    else:

                        # -------------------------
                        # WITH GROUP
                        # -------------------------
                        if group_col != "Sin grupo":

                            chart_df = (
                                chart_df
                                .groupby([x_col, group_col])[y_col]
                                .agg(aggregation)
                                .reset_index()
                            )

                        # -------------------------
                        # WITHOUT GROUP
                        # -------------------------
                        else:

                            chart_df = (
                                chart_df
                                .groupby(x_col)[y_col]
                                .agg(aggregation)
                                .reset_index()
                            )

                        y_axis = y_col

                # ==================================================
                # NO AGGREGATION
                # ==================================================
                else:

                    y_axis = y_col

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
                else:

                    fig = px.scatter(
                        chart_df,
                        x=x_col,
                        y=y_axis,
                        color=None
                        if group_col == "Sin grupo"
                        else group_col
                    )

                # ==================================================
                # RENDER
                # ==================================================
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                # ==================================================
                # SHOW DATA
                # ==================================================
                with st.expander("📄 Ver datos"):

                    st.dataframe(
                        chart_df,
                        use_container_width=True
                    )

            except Exception as e:

                st.error(f"Error generando gráfico: {e}")

    # ==================================================
    # 📊 BAR
    # ==================================================
    with tabs[1]:

        cat_col = st.selectbox(
            "Categoría",
            columns,
            key="bar_cat"
        )

        value_col = st.selectbox(
            "Valor",
            columns,
            key="bar_value"
        )

        if st.button(
            "Generar gráfico",
            key="btn_bar_chart"
        ):

            try:

                bar_df = (
                    df.groupby(cat_col)[value_col]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )

                fig = px.bar(
                    bar_df,
                    x=cat_col,
                    y=value_col
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Error generando gráfico: {e}")

    # ==================================================
    # 🥧 PIE
    # ==================================================
    with tabs[2]:

        pie_col = st.selectbox(
            "Segmento",
            columns,
            key="pie_segment"
        )

        pie_value = st.selectbox(
            "Valor",
            columns,
            key="pie_value"
        )

        if st.button(
            "Generar gráfico",
            key="btn_pie_chart"
        ):

            try:

                pie_data = (
                    df.groupby(pie_col)[pie_value]
                    .sum()
                    .reset_index()
                )

                fig = px.pie(
                    pie_data,
                    names=pie_col,
                    values=pie_value
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Error generando gráfico: {e}")

    # ==================================================
    # 📉 FORECAST
    # ==================================================
    with tabs[3]:

        forecast_col = st.selectbox(
            "Serie",
            columns,
            key="forecast_series"
        )

        if st.button(
            "Generar forecast",
            key="btn_forecast"
        ):

            try:

                fig = px.line(
                    df,
                    y=forecast_col
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Error generando forecast: {e}")