import streamlit as st

from ui.services.dataset_service import (
    DatasetService
)

from ui.components.dataset_row import (
    render_dataset_row
)


def render_datasets():

    st.title(
        "📚 Dataset Management"
    )

    datasets = (
        DatasetService.list_available()
    )

    if not datasets:

        st.info(
            "No datasets available"
        )

        return

    st.markdown("---")

    for dataset in datasets:

        render_dataset_row(
            dataset
        )