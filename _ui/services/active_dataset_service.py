import streamlit as st


class ActiveDatasetService:

    @staticmethod
    def add(
        dataset_name: str
    ):

        st.session_state.setdefault(
            "active_datasets",
            []
        )

        if (
            dataset_name
            not in st.session_state[
                "active_datasets"
            ]
        ):

            st.session_state[
                "active_datasets"
            ].append(
                dataset_name
            )

    @staticmethod
    def remove(
        dataset_name: str
    ):

        st.session_state.setdefault(
            "active_datasets",
            []
        )

        if (
            dataset_name
            in st.session_state[
                "active_datasets"
            ]
        ):

            st.session_state[
                "active_datasets"
            ].remove(
                dataset_name
            )