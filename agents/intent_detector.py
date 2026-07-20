import json
import re

from agents.filters import normalize_query_for_intent
from semantic.semantic_layer import detect_dimension, detect_metric


INTENT_KEYWORDS = {
    "top": ["top", "mas", "mayores"],
    "bottom": ["bottom", "menos", "peores"],
    "average": ["promedio", "average"],
    "total": ["total", "suma"],
}

UNKNOWN_INTENT = {
    "intent": "unknown",
    "metric": None,
    "dimension": None,
    "limit": None,
}


def normalize_intent(intent: dict) -> dict:
    return {
        "intent": intent.get("intent"),
        "metric": intent.get("metric"),
        "dimension": intent.get("dimension"),
        "limit": int(intent.get("limit")) if intent.get("limit") else None,
    }


def detect_fast_intent(query: str) -> str | None:
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in query for keyword in keywords):
            return intent
    return None


def detect_limit(query: str) -> int | None:
    match = re.search(r"\b(\d+)\b", query)
    return int(match.group(1)) if match else None


def build_llm_prompt(question: str) -> str:
    return f"""
Classify the user intent.

Return ONLY JSON:

{{
  "intent": "top | bottom | average | total | comparison | distribution | unknown",
  "metric": "string or null",
  "dimension": "string or null",
  "limit": "number or null"
}}

Question:
{question}
"""


def detect_llm_intent(question: str, llm) -> dict:
    raw = llm.generate(
        build_llm_prompt(question),
        system_prompt="Intent classifier",
    )

    try:
        return normalize_intent(json.loads(raw))
    except (json.JSONDecodeError, TypeError, ValueError):
        return UNKNOWN_INTENT.copy()


def detect_intent(question: str, llm, semantic_layer=None) -> dict:
    query = normalize_query_for_intent(question)

    intent = detect_fast_intent(query)
    limit = detect_limit(query)

    metric = detect_metric(query, semantic_layer)
    dimension = detect_dimension(query, semantic_layer)

    if intent:
        return normalize_intent(
            {
                "intent": intent,
                "metric": metric,
                "dimension": dimension,
                "limit": limit,
            }
        )

    return detect_llm_intent(question, llm)