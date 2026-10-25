import streamlit as st
from ui.services.dataset_service import DatasetService
from ui.services.active_dataset_service import ActiveDatasetService


def render_dataset_panel():

    active_datasets = st.session_state.setdefault(
        "active_datasets",
        []
    )

    available_datasets = (
        DatasetService.list_available()
    )

    with st.expander(
        "📚 Available Datasets",
        expanded=False
    ):

        for dataset in available_datasets:
            render_dataset_row(
                dataset,
                active_datasets
            )

    render_active_summary(
        active_datasets
    )


def render_dataset_row(
    dataset,
    active_datasets
):

    col1, col2, col3 = (
        st.columns([4, 1, 1])
    )

    is_active = (
        dataset in active_datasets
    )

    with col1:
        st.write(dataset)

    with col2:

        if is_active:

            st.success(
                "Active"
            )

        elif st.button(
            "Add",
            key=f"add_{dataset}"
        ):

            ActiveDatasetService.add(
                dataset
            )

            st.rerun()

    with col3:

        if not is_active:
            return

        if st.button(
            "Remove",
            key=f"remove_{dataset}"
        ):

            ActiveDatasetService.remove(
                dataset
            )

            st.rerun()


def render_active_summary(
    active_datasets
):

    if active_datasets:

        st.info(
            "📚 Active datasets: "
            + ", ".join(
                active_datasets
            )
        )

        return

    st.warning(
        "No datasets selected."
    )