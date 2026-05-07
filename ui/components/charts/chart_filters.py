import streamlit as st


def render_filters(df):

    columns = list(df.columns)

    st.subheader("🎯 Filtros")

    filter_col = st.selectbox(
        "Filtrar por",
        ["Sin filtro"] + columns
    )

    if filter_col == "Sin filtro":

        return None

    unique_values = (
        df[filter_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_values = st.multiselect(
        "Valores",
        unique_values,
        default=unique_values[:5]
        if len(unique_values) > 5
        else unique_values
    )

    return {
        "column": filter_col,
        "values": selected_values
    }


def apply_filters(df, filters):

    if not filters:

        return df

    return df[
        df[filters["column"]]
        .isin(filters["values"])
    ]