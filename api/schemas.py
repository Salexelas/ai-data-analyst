from pydantic import BaseModel

from typing import Optional, Any, Union


class QueryRequest(BaseModel):

    question: str

    dataset_ids: list[str]

    dataset_relations: Optional[list[dict]] = None

    semantic_layer: Optional[dict[str, Any]] = None

    inline_datasets: Optional[
        dict[str, list[dict[str, Any]]]
    ] = None

    inline_dataset_schema: Optional[
        dict[str, dict[str, str]]
    ] = None

    taxonomies: Optional[dict[str, Any]] = None

    examples: Optional[
        Union[
            list[dict[str, Any]],
            dict[str, Any],
        ]
    ] = None