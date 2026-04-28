from dataclasses import dataclass, field
from typing import Any
import pandas as pd

@dataclass
class InputContext:
    question: str
    connector: Any
    semantic_layer: dict | None
    llm: Any

@dataclass
class ExecutionContext:
    schema: Any = None
    columns: list | None = None
    sql: str | None = None
    language: str = "en"
    intent: dict | None = None   # 🔥 NUEVO

@dataclass
class OutputContext:
    result: pd.DataFrame | None = None
    insight: str | None = None

@dataclass
class QueryContext:
    input: InputContext
    exec: ExecutionContext = field(default_factory=ExecutionContext)
    output: OutputContext = field(default_factory=OutputContext)
    trace_id: str | None = None