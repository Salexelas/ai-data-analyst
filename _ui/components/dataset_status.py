import streamlit as st

from ui.services.dataset_service import (
    DatasetService
)


def render_dataset_status(
    dataset_name: str
):

    path = (
        DatasetService.get_path(
            dataset_name
        )
    )

    st.write(
        f"📄 {dataset_name}"
    )

    if (
        st.session_state.get(
            "file_path"
        )
        == path
    ):

        st.caption(
            "🟢 Active Dataset"
        )