import streamlit as st


def build_forecast_config(df):

    columns = list(df.columns)

    x_col = st.selectbox(
        "Fecha",
        columns
    )

    y_col = st.selectbox(
        "Serie",
        columns
    )

    periods = st.slider(
        "Períodos futuros",
        1,
        365,
        30
    )

    return {

        "x": x_col,
        "y": y_col,
        "periods": periods
    }