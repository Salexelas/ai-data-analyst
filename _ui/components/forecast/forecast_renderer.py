import streamlit as st
import plotly.express as px
import pandas as pd

from ui.components.forecast.forecast_models import (
    simple_forecast
)


def render_forecast_chart(df, config):

    if not st.button("Generar forecast"):

        return

    try:

        x_col = config["x"]
        y_col = config["y"]
        periods = config["periods"]

        forecast_df = simple_forecast(
            df,
            y_col,
            periods
        )

        fig = px.line(
            df,
            x=x_col,
            y=y_col
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        with st.expander("📄 Forecast"):

            st.dataframe(
                forecast_df,
                width="stretch"
            )

    except Exception as e:

        st.error(f"Error generando forecast: {e}")