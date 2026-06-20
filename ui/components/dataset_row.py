import streamlit as st

from ui.components.dataset_status import (
    render_dataset_status
)

from ui.components.dataset_actions import (
    render_dataset_actions
)

from ui.components.dataset_preview import (
    render_dataset_preview
)


def render_dataset_row(
    dataset_name: str
):

    col1, col2 = st.columns(
        [4, 2]
    )

    with col1:

        render_dataset_status(
            dataset_name
        )

    with col2:

        render_dataset_actions(
            dataset_name
        )

    render_dataset_preview(
        dataset_name
    )