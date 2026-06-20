import streamlit as st

from ui.services.dataset_service import (
    DatasetService
)

from ui.services.active_dataset_service import (
    ActiveDatasetService
)


def render_dataset_panel():

    st.session_state.setdefault(
        "active_datasets",
        []
    )

    active_datasets = (
        st.session_state[
            "active_datasets"
        ]
    )

    available_datasets = (
        DatasetService.list_available()
    )

    with st.expander(
        "📚 Available Datasets",
        expanded=False
    ):

        for dataset in available_datasets:

            col1, col2, col3 = (
                st.columns([4, 1, 1])
            )

            with col1:

                st.write(
                    dataset
                )

            with col2:

                if dataset in active_datasets:

                    st.success(
                        "Active"
                    )

                else:

                    if st.button(
                        "Add",
                        key=f"add_{dataset}"
                    ):

                        ActiveDatasetService.add(
                            dataset
                        )

                        st.rerun()

            with col3:

                if dataset in active_datasets:

                    if st.button(
                        "Remove",
                        key=f"remove_{dataset}"
                    ):

                        ActiveDatasetService.remove(
                            dataset
                        )

                        st.rerun()

    if active_datasets:

        st.info(
            "📚 Active datasets: "
            + ", ".join(
                active_datasets
            )
        )

    else:

        st.warning(
            "No datasets selected."
        )