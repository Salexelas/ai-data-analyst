from connectors.factory import (
    create_connector
)

from ui.services.dataset_service import (
    DatasetService
)

from core.utils.file_type_detector import (
    FileTypeDetector
)


class DatasetLoader:

    @staticmethod
    def load(
        dataset_name: str
    ):

        file_type = (
            FileTypeDetector.detect(
                dataset_name
            )
        )

        if not file_type:

            raise ValueError(
                "Unsupported file format"
            )

        path = (
            DatasetService.get_path(
                dataset_name
            )
        )

        return create_connector(
            file_type,
            {
                "file_path": path
            }
        )