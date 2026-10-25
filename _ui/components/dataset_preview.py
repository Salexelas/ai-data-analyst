import streamlit as st

from ui.services.preview_service import (
    PreviewService
)


def render_dataset_preview(
    dataset_name: str
):

    with st.expander(
        f"Preview: {dataset_name}"
    ):

        try:

            preview = (
                PreviewService.get_preview(
                    dataset_name
                )
            )

            st.dataframe(
                preview,
                width="stretch"
            )

        except Exception as e:

            st.error(
                str(e)
            )