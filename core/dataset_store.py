class DatasetStore:
    _registry = {}

    @classmethod
    def register(cls, dataset_id: str, semantic_layer: dict) -> None:
        """Registra o actualiza la capa semántica completa de un dataset."""
        cls._registry[dataset_id] = semantic_layer

    @classmethod
    def get(cls, dataset_id: str) -> dict:
        """Obtiene la capa semántica precargada."""
        return cls._registry.get(dataset_id, {})

    @classmethod
    def exists(cls, dataset_id: str) -> bool:
        return dataset_id in cls._registry