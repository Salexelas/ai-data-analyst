from connectors.factory import (
    create_connector
)

from semantic.utils import (
    get_dataset_id
)

from services.semantic_service import (
    SemanticService
)

from core.session_manager import (
    SessionManager
)


class SourceService:

    @staticmethod
    def register(
        source_type,
        config
    ):

        connector = create_connector(
            source_type,
            config
        )

        dataset_id = get_dataset_id(
            source_type,
            config
        )

        semantic_layer = (
            SemanticService.load(
                dataset_id
            )
        )

        SessionManager.set(
            "connector",
            connector
        )

        SessionManager.set(
            "dataset_id",
            dataset_id
        )

        if semantic_layer:

            SessionManager.set(
                "semantic_layer",
                semantic_layer
            )

        return dataset_id