from semantic.utils import (
    load_semantic_layer
)


class SemanticService:

    @staticmethod
    def load(
        dataset_id
    ):

        return load_semantic_layer(
            dataset_id
        )