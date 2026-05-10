import streamlit as st


def render_analytics(response):

    # -------------------------
    # EXECUTIVE MARKDOWN
    # -------------------------
    if response.markdown:

        st.markdown(
            response.markdown
        )

    # -------------------------
    # METRICS
    # -------------------------
    if response.metrics:

        st.markdown("## 📌 KPIs")

        cols = st.columns(
            len(response.metrics)
        )

        for col, (k, v) in zip(
            cols,
            response.metrics.items()
        ):

            col.metric(k, v)

    # -------------------------
    # DATAFRAME
    # -------------------------
    if response.data is not None:

        st.markdown("## 📊 Datos")

        st.dataframe(
            response.data
        )

    # -------------------------
    # CHARTS
    # -------------------------
    if response.chart_type == "line":

        st.line_chart(
            response.data
        )

    elif response.chart_type == "bar":

        st.bar_chart(
            response.data
        )

    # -------------------------
    # SQL
    # -------------------------
    if response.sql:

        with st.expander(
            "🛠 SQL"
        ):

            st.code(
                response.sql,
                language="sql"
            )