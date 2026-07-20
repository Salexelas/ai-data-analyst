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

    with tabs[0]:
        render_general_tab(df)

    with tabs[1]:
        render_schema_tab(df)

    with tabs[2]:
        render_numeric_tab(numeric_df)

    with tabs[3]:
        render_categorical_tab(cat_df)

    with tabs[4]:
        render_correlation_tab(numeric_df)

    with tabs[5]:
        render_raw_tab(df)


def render_general_tab(df):

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows (sample)", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Missing", int(df.isna().sum().sum()))

    memory_mb = round(
        df.memory_usage(deep=True).sum() / 1024 / 1024,
        2
    )

    col4.metric("Memory MB", memory_mb)


def render_schema_tab(df):

    schema_df = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str),
        "nulls": df.isna().sum().values,
        "unique": df.nunique().values
    })

    st.dataframe(schema_df, width="stretch")


def render_numeric_tab(numeric_df):

    if numeric_df.empty:
        st.info("No hay columnas numéricas")
        return

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


def render_categorical_tab(cat_df):

    if cat_df.empty:
        st.info("No hay columnas categóricas")
        return

    for col in cat_df.columns[:5]:

        st.subheader(col)

        st.bar_chart(
            cat_df[col]
            .astype(str)
            .value_counts()
            .head(10)
        )


def render_correlation_tab(numeric_df):

    if len(numeric_df.columns) <= 1:
        st.info("No hay suficientes columnas numéricas")
        return

    corr = numeric_df.corr(numeric_only=True)

    st.dataframe(
        corr.round(2),
        width="stretch"
    )


def render_raw_tab(df):

    st.dataframe(
        df.head(100),
        width="stretch"
    )