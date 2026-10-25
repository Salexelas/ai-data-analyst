from dataclasses import dataclass, field


@dataclass
class DatasetRelationship:
    left_dataset: str
    left_column: str
    right_dataset: str
    right_column: str


@dataclass
class ChatSession:
    active_datasets: list[str] = field(default_factory=list)

    dataset_relations: list[
        DatasetRelationship
    ] = field(default_factory=list)

    semantic_layer: dict | None = None