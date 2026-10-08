'''from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class AnalyticsResponse:

    type: str

    markdown: str

    data: Any = None

    sql: Optional[str] = None

    chart_type: Optional[str] = None

    language: Optional[str] = "es"

    metrics: Optional[dict] = None

    severity: Optional[str] = None'''