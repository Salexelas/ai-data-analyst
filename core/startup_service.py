import os
import streamlit as st

from connectors.factory import create_connector

DATA_PATH = "data"


def autoload_last_dataset():

    if st.session_state["connector"] is not None:
        return

    if not os.path.exists(DATA_PATH):
        return

    files = sorted(os.listdir(DATA_PATH), reverse=True)

    if not files:
        return

    last_file = files[0]
    file_path = os.path.join(DATA_PATH, last_file)

    if last_file.endswith(".csv"):
        file_type = "csv"

    elif last_file.endswith(".xlsx"):
        file_type = "excel"

    else:
        return

    try:

        connector = create_connector(
            file_type,
            {"file_path": file_path}
        )

        st.session_state["connector"] = connector
        st.session_state["file_path"] = file_path
        st.session_state["dataset_id"] = last_file

    except Exception as e:
        st.warning(f"No se pudo cargar dataset: {e}")