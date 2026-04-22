from dataclasses import dataclass
from typing import Any
import pandas as pd


@dataclass
class QueryContext:
    question: str
    connector: any
    semantic_layer: dict | None = None

    schema: any = None
    columns: list | None = None
    sql: str | None = None
    result: pd.DataFrame | None = None
    insight: str | None = None

    llm: any = None 
    language: str | None = None