'''import os
import streamlit as st

from connectors.factory import create_connector

DATA_PATH = "data"

FILE_TYPES = {
    ".csv": "csv",
    ".xlsx": "excel",
}


def get_last_dataset():

    if not os.path.exists(DATA_PATH):
        return None

    files = sorted(os.listdir(DATA_PATH), reverse=True)

    if not files:
        return None

    dataset_id = files[0]

    file_type = FILE_TYPES.get(
        os.path.splitext(dataset_id)[1]
    )

    if not file_type:
        return None

    return (
        file_type,
        os.path.join(DATA_PATH, dataset_id),
        dataset_id,
    )


def load_dataset(file_type, file_path, dataset_id):

    st.session_state["connector"] = create_connector(
        file_type,
        {"file_path": file_path},
    )

    st.session_state["file_path"] = file_path
    st.session_state["dataset_id"] = dataset_id


def autoload_last_dataset():

    if st.session_state["connector"] is not None:
        return

    dataset = get_last_dataset()

    if dataset is None:
        return

    try:
        load_dataset(*dataset)
    except Exception as e:
        st.warning(f"No se pudo cargar dataset: {e}")'''