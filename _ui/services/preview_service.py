from connectors.factory import (
    create_connector
)

from ui.services.dataset_service import (
    DatasetService
)

from core.utils.file_type_detector import (
    FileTypeDetector
)


class PreviewService:

    @staticmethod
    def get_preview(
        dataset_name: str
    ):

        file_type = (
            FileTypeDetector.detect(
                dataset_name
            )
        )

        connector = create_connector(
            file_type,
            {
                "file_path":
                    DatasetService.get_path(
                        dataset_name
                    )
            }
        )

        return connector.preview()