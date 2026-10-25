from ui.services.dataset_loader import (
    DatasetLoader
)

from ui.services.dataset_service import (
    DatasetService
)

from ui.services.dataset_state_service import (
    DatasetStateService
)


class DatasetActivationService:

    @staticmethod
    def activate(
        dataset_name: str
    ):

        connector = (
            DatasetLoader.load(
                dataset_name
            )
        )

        path = (
            DatasetService.get_path(
                dataset_name
            )
        )

        DatasetStateService.set_active_connector(
            connector=connector,
            dataset_name=dataset_name,
            path=path,
        )