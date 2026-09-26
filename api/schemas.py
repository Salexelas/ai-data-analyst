from pydantic import BaseModel
from typing import Optional, Any

class QueryRequest(BaseModel):
    question: str
    dataset_ids: list[str]
    dataset_relations: Optional[list[dict]] = None
    semantic_layer: Optional[dict] = None
    inline_datasets: Optional[dict[str, list[dict[str, Any]]]] = None