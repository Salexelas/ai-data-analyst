import streamlit as st
import pandas as pd


def render_dataset_info():

    st.title("📊 Dataset Analytics")

    if "connector" not in st.session_state:

        st.warning(
            "No hay dataset cargado"
        )

        return

    connector = st.session_state["connector"]

    # 🔥 dataframe REAL
    df = connector.preview(limit=100000)

    st.markdown("---")

    # =========================
    # GENERAL
    # =========================

    st.subheader(
        "📌 Información General"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        len(df)
    )

    col2.metric(
        "Columns",
        len(df.columns)
    )

    col3.metric(
        "Missing",
        int(df.isna().sum().sum())
    )

    memory_mb = round(
        df.memory_usage(deep=True).sum()
        / 1024 / 1024,
        2
    )

    col4.metric(
        "Memory MB",
        memory_mb
    )

    st.markdown("---")

    # =========================
    # SCHEMA
    # =========================

    st.subheader(
        "🧬 Schema"
    )

    schema_df = pd.DataFrame({

        "column": df.columns,

        "dtype": df.dtypes.astype(str),

        "nulls": df.isna().sum().values,

        "unique": df.nunique().values
    })

    st.dataframe(
        schema_df,
        use_container_width=True
    )

    st.markdown("---")

    # =========================
    # NUMERIC
    # =========================

    numeric_df = df.select_dtypes(
        include="number"
    )

    if not numeric_df.empty:

        st.subheader(
            "📈 Numeric Analytics"
        )

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
            use_container_width=True
        )

        st.bar_chart(
            numeric_df.mean()
        )

    st.markdown("---")

    # =========================
    # CATEGORICAL
    # =========================

    cat_df = df.select_dtypes(
        exclude="number"
    )

    if not cat_df.empty:

        st.subheader(
            "🏷 Variables categóricas"
        )

        for col in cat_df.columns[:5]:

            st.markdown(f"### {col}")

            vc = (
                cat_df[col]
                .astype(str)
                .value_counts()
                .head(10)
            )

            st.bar_chart(vc)

    st.markdown("---")

    # =========================
    # CORRELATION
    # =========================

    if len(numeric_df.columns) > 1:

        st.subheader(
            "🔥 Correlaciones"
        )

        corr = numeric_df.corr(
            numeric_only=True
        )

        st.dataframe(
            corr.round(2),
            use_container_width=True
        )

    st.markdown("---")

    # =========================
    # RAW
    # =========================

    st.subheader("📄 Raw Data")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )