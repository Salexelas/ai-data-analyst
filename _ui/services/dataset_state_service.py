import streamlit as st


class DatasetStateService:

    @staticmethod
    def set_active_connector(
        connector,
        dataset_name,
        path,
    ):

        st.session_state[
            "connector"
        ] = connector

        st.session_state[
            "file_path"
        ] = path

        st.session_state[
            "dataset_id"
        ] = dataset_name

    @staticmethod
    def clear_active_dataset():

        st.session_state[
            "connector"
        ] = None

        st.session_state[
            "file_path"
        ] = None

        st.session_state[
            "dataset_id"
        ] = None

        st.session_state[
            "semantic_layer"
        ] = None