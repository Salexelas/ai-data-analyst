import streamlit as st

from ui.services.dataset_activation_service import (
    DatasetActivationService
)
from ui.services.dataset_delete_service import (
    DatasetDeleteService
)


def render_dataset_actions(dataset_name: str):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_action_button(
            "Load",
            f"load_{dataset_name}",
            lambda: DatasetActivationService.activate(
                dataset_name
            ),
        )

    with col2:
        render_action_button(
            "Edit",
            f"edit_{dataset_name}",
            lambda: edit_dataset(dataset_name),
        )

    with col3:
        render_action_button(
            "Info",
            f"info_{dataset_name}",
            lambda: show_dataset_info(dataset_name),
        )

    with col4:
        render_action_button(
            "🗑️",
            f"delete_{dataset_name}",
            lambda: DatasetDeleteService.delete(
                dataset_name
            ),
        )


def render_action_button(
    label: str,
    key: str,
    action,
):

    if not st.button(label, key=key):
        return

    try:
        action()
        st.rerun()

    except Exception as e:
        st.error(str(e))


def edit_dataset(dataset_name: str):

    DatasetActivationService.activate(
        dataset_name
    )

    st.session_state.page = (
        "dataset_editor"
    )


def show_dataset_info(dataset_name: str):

    DatasetActivationService.activate(
        dataset_name
    )

    st.session_state.page = (
        "dataset_info"
    )