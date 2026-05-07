import streamlit as st

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
    # LOAD DATAFRAME
    # ==================================================
    try:

        df = connector.preview(100000)

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
        "📈 Línea",
        "📊 Barras",
        "🥧 Torta",
        "📉 Forecast"
    ])

    # ==================================================
    # 📈 LINE
    # ==================================================
    with tabs[0]:

        x_col = st.selectbox(
            "Eje X",
            columns,
            key="line_x"
        )

        y_col = st.selectbox(
            "Eje Y",
            columns,
            key="line_y"
        )

        if st.button(
            "Generar gráfico",
            key="btn_line_chart"
        ):

            st.line_chart(
                df.set_index(x_col)[y_col]
            )

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

            st.bar_chart(
                df.set_index(cat_col)[value_col]
            )

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

            pie_data = (
                df.groupby(pie_col)[pie_value]
                .sum()
            )

            st.write(pie_data)

            # después podés usar plotly

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

            st.line_chart(
                df[forecast_col]
            )