import os
import streamlit as st

from ui.services.dataset_service import (
    DatasetService
)

from ui.services.dataset_state_service import (
    DatasetStateService
)


class DatasetDeleteService:

    @staticmethod
    def delete(
        dataset_name: str
    ):

        path = (
            DatasetService.get_path(
                dataset_name
            )
        )

        os.remove(path)

        current_path = (
            st.session_state.get(
                "file_path"
            )
        )

        if current_path == path:

            DatasetStateService.clear_active_dataset()