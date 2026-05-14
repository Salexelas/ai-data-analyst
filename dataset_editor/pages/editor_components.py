import os
import streamlit as st

from dataset_editor.services.type_service import TYPE_OPTIONS


def validate_dataset():

    file_path = st.session_state.get("file_path")

    if not file_path:
        st.warning("Primero cargá un dataset")
        return None

    if not os.path.exists(file_path):
        st.error("El archivo no existe")
        return None

    return file_path


def load_dataset(service, file_path):

    try:
        return service.load_preview(file_path, limit=1000)

    except Exception as e:
        st.error(f"Error cargando dataset: {e}")
        return None


def render_tabs(service, df, schema):

    tabs = st.tabs([
        "📝 Columnas",
        "🧠 Tipos",
        "📊 Datos"
    ])

    with tabs[0]:
        rename_map = render_columns_tab(df)

    with tabs[1]:
        column_types = render_types_tab(service, df, schema)

    typed_df = service.apply_types(df, column_types)

    with tabs[2]:
        edited_df = render_data_tab(typed_df)

    edited_df.columns = [
        rename_map[c]
        for c in edited_df.columns
    ]

    return rename_map, column_types, edited_df


def render_columns_tab(df):

    rename_map = {}
    cols = st.columns(2)

    for i, col in enumerate(df.columns):

        with cols[i % 2]:
            rename_map[col] = st.text_input(
                col,
                value=col,
                key=f"rename_{col}"
            )

    return rename_map


def render_types_tab(service, df, schema):

    column_types = {}
    cols = st.columns(2)

    for i, col in enumerate(df.columns):

        with cols[i % 2]:

            saved_type = schema.get(col)

            default_type = (
                saved_type
                if saved_type
                else service.detect_type(df[col])
            )

            column_types[col] = st.selectbox(
                f"Tipo → {col}",
                TYPE_OPTIONS,
                index=TYPE_OPTIONS.index(default_type),
                key=f"type_{col}"
            )

    return column_types


def render_data_tab(df):

    return st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        height=600
    )


def save_changes(service, file_path, edited_df, rename_map, column_types):

    try:

        service.save_dataset(
            edited_df,
            file_path
        )

        updated_schema = service.build_updated_schema(
            rename_map,
            column_types
        )

        service.save_schema(
            file_path,
            updated_schema
        )

        st.session_state["semantic_layer"] = None

        st.success("✅ Dataset actualizado")
        st.rerun()

    except Exception as e:
        st.error(f"Error guardando dataset: {e}")