import streamlit as st
import pandas as pd

from dataset_editor.adapters.pandas_adapter import PandasAdapter


adapter = PandasAdapter()


def render_dataset_info():

    st.title("📊 Dataset Analytics")

    file_path = st.session_state.get("file_path")

    if not file_path:
        st.warning("No hay dataset cargado")
        return

    try:
        # muestra razonable para análisis UI
        df = adapter.load_preview(file_path, limit=5000)

    except Exception as e:
        st.error(f"Error cargando dataset: {e}")
        return

    numeric_df = df.select_dtypes(include="number")
    cat_df = df.select_dtypes(exclude="number")

    tabs = st.tabs([
        "📌 General",
        "🧬 Schema",
        "📈 Numérico",
        "🏷 Categórico",
        "🔥 Correlaciones",
        "📄 Raw"
    ])

    # GENERAL
    with tabs[0]:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows (sample)", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric("Missing", int(df.isna().sum().sum()))

        memory_mb = round(
            df.memory_usage(deep=True).sum() / 1024 / 1024,
            2
        )

        col4.metric("Memory MB", memory_mb)

    # SCHEMA
    with tabs[1]:

        schema_df = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str),
            "nulls": df.isna().sum().values,
            "unique": df.nunique().values
        })

        st.dataframe(
            schema_df,
            width="stretch"
        )

    # NUMERIC
    with tabs[2]:

        if numeric_df.empty:
            st.info("No hay columnas numéricas")

        else:

            stats = pd.DataFrame({
                "mean": numeric_df.mean(),
                "median": numeric_df.median(),
                "std": numeric_df.std(),
                "min": numeric_df.min(),
                "max": numeric_df.max(),
                "missing": numeric_df.isna().sum()
            })

            st.dataframe(
                stats.round(2),
                width="stretch"
            )

            st.bar_chart(numeric_df.mean())

    # CATEGORICAL
    with tabs[3]:

        if cat_df.empty:
            st.info("No hay columnas categóricas")

        else:

            for col in cat_df.columns[:5]:

                st.subheader(col)

                vc = (
                    cat_df[col]
                    .astype(str)
                    .value_counts()
                    .head(10)
                )

                st.bar_chart(vc)

    # CORRELATION
    with tabs[4]:

        if len(numeric_df.columns) <= 1:
            st.info("No hay suficientes columnas numéricas")

        else:

            corr = numeric_df.corr(numeric_only=True)

            st.dataframe(
                corr.round(2),
                width="stretch"
            )

    # RAW
    with tabs[5]:

        st.dataframe(
            df.head(100),
            width="stretch"
        )