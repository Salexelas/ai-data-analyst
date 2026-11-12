from pydantic import BaseModel, Field
from typing import Optional, Any, Union


class QueryRequest(BaseModel):
    question: str
    dataset_ids: list[str] = Field(default_factory=list)
    dataset_relations: Optional[list[dict]] = None
    semantic_layer: Optional[dict[str, Any]] = None
    inline_datasets: Optional[dict[str, list[dict[str, Any]]]] = None
    inline_dataset_schema: Optional[dict[str, dict[str, str]]] = None
    taxonomies: Optional[dict[str, Any]] = None
    examples: Optional[Union[list[dict[str, Any]], dict[str, Any]]] = None
    
    # Nuevos campos para base de datos externa
    db_connection_url: Optional[str] = None
    db_schema: Optional[str] = None


class ConnectionTestRequest(BaseModel):
    db_connection_url: str
    db_schema: Optional[str] = None


class ClientCreateRequest(BaseModel):
    name: str
    slug: str


class ClientResponse(BaseModel):
    id: str
    name: str
    slug: str