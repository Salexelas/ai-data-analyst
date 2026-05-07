import streamlit as st
import pandas as pd
import os

from connectors.factory import create_connector

DATA_PATH = "data"


def render_dataset_editor():

    st.title("✏️ Editor de Dataset")

    file_path = st.session_state.get("file_path")

    if not file_path:
        st.warning("Primero cargá un dataset")
        return

    if not os.path.exists(file_path):
        st.error("El archivo no existe")
        return

    file_name = os.path.basename(file_path)

    # -------------------------
    # Detect file type
    # -------------------------
    if file_name.endswith(".csv"):
        file_type = "csv"

    elif file_name.endswith(".xlsx"):
        file_type = "excel"

    else:
        st.error("Formato no soportado")
        return

    # -------------------------
    # Load dataframe
    # -------------------------
    try:

        connector = create_connector(
            file_type,
            {"file_path": file_path}
        )

        df = connector.preview(100000)

    except Exception as e:

        st.error(f"Error cargando dataset: {e}")
        return

    # -------------------------
    # Rename columns
    # -------------------------
    st.subheader("📝 Renombrar columnas")

    rename_map = {}

    cols = st.columns(2)

    for i, col in enumerate(df.columns):

        with cols[i % 2]:

            new_name = st.text_input(
                f"{col}",
                value=col,
                key=f"rename_{col}"
            )

            rename_map[col] = new_name

    # -------------------------
    # Editable dataframe
    # -------------------------
    st.subheader("📊 Editor")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        height=600
    )

    # -------------------------
    # Apply renamed columns
    # -------------------------
    edited_df.columns = [
        rename_map[c]
        for c in edited_df.columns
    ]

    # -------------------------
    # Save
    # -------------------------
    if st.button("💾 Guardar cambios"):

        try:

            if file_type == "csv":

                edited_df.to_csv(
                    file_path,
                    index=False
                )

            else:

                edited_df.to_excel(
                    file_path,
                    index=False
                )

            # -------------------------
            # Reload connector
            # -------------------------
            connector = create_connector(
                file_type,
                {"file_path": file_path}
            )

            st.session_state["connector"] = connector

            # ⚠️ invalidar semantic layer
            st.session_state["semantic_layer"] = None

            st.success("✅ Dataset actualizado")

            st.rerun()

        except Exception as e:

            st.error(f"Error guardando dataset: {e}")