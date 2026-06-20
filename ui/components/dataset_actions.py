import streamlit as st

from ui.services.dataset_activation_service import (
    DatasetActivationService
)

from ui.services.dataset_delete_service import (
    DatasetDeleteService
)


def render_dataset_actions(
    dataset_name: str
):

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    # -------------------------
    # LOAD
    # -------------------------

    with col1:

        if st.button(
            "Load",
            key=f"load_{dataset_name}"
        ):

            try:

                DatasetActivationService.activate(
                    dataset_name
                )

                st.rerun()

            except Exception as e:

                st.error(
                    str(e)
                )

    # -------------------------
    # EDIT
    # -------------------------

    with col2:

        if st.button(
            "Edit",
            key=f"edit_{dataset_name}"
        ):

            try:

                DatasetActivationService.activate(
                    dataset_name
                )

                st.session_state.page = (
                    "dataset_editor"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    str(e)
                )

    # -------------------------
    # INFO
    # -------------------------

    with col3:

        if st.button(
            "Info",
            key=f"info_{dataset_name}"
        ):

            try:

                DatasetActivationService.activate(
                    dataset_name
                )

                st.session_state.page = (
                    "dataset_info"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    str(e)
                )

    # -------------------------
    # DELETE
    # -------------------------

    with col4:

        if st.button(
            "🗑️",
            key=f"delete_{dataset_name}"
        ):

            try:

                DatasetDeleteService.delete(
                    dataset_name
                )

                st.rerun()

            except Exception as e:

                st.error(
                    str(e)
                )