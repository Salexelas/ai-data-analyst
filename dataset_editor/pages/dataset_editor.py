import streamlit as st

from dataset_editor.services.editor_service import EditorService
from dataset_editor.pages.editor_components import (
    validate_dataset,
    load_dataset,
    render_tabs,
    save_changes
)

service = EditorService()


def render_dataset_editor():

    st.title("✏️ Editor de Dataset")

    file_path = validate_dataset()

    if not file_path:
        return

    df = load_dataset(service, file_path)

    if df is None:
        return

    schema = service.load_schema(file_path)

    rename_map, column_types, edited_df = render_tabs(
        service,
        df,
        schema
    )

    st.divider()

    if st.button("💾 Guardar cambios"):
        save_changes(
            service,
            file_path,
            edited_df,
            rename_map,
            column_types
        )