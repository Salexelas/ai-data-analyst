import json
import re
from agents.filters import normalize_query_for_intent
from semantic.semantic_layer import detect_metric, detect_dimension


def normalize_intent(intent: dict):
    return {
        "intent": intent.get("intent"),
        "metric": intent.get("metric"),
        "dimension": intent.get("dimension"),
        "limit": int(intent.get("limit")) if intent.get("limit") else None
    }

def detect_intent(question: str, llm, semantic_layer=None):

    q = normalize_query_for_intent(question)

    # -------------------------
    # INTENT
    # -------------------------
    if any(x in q for x in ["top", "mas", "mayores"]):
        intent = "top"
    elif any(x in q for x in ["bottom", "menos", "peores"]):
        intent = "bottom"
    elif any(x in q for x in ["promedio", "average"]):
        intent = "average"
    elif any(x in q for x in ["total", "suma"]):
        intent = "total"
    else:
        intent = None

    # -------------------------
    # LIMIT
    # -------------------------
    limit_match = re.search(r"\b(\d+)\b", q)
    limit = int(limit_match.group(1)) if limit_match else None

    # -------------------------
    # 🔥 METRIC + DIMENSION (GENÉRICO)
    # -------------------------
    metric = detect_metric(q, semantic_layer)
    dimension = detect_dimension(q, semantic_layer)

    # -------------------------
    # FAST PATH
    # -------------------------
    if intent:
        return normalize_intent({
            "intent": intent,
            "metric": metric,
            "dimension": dimension,
            "limit": limit
        })

    # -------------------------
    # FALLBACK LLM
    # -------------------------
    prompt = f"""
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

    raw = llm.generate(prompt, system_prompt="Intent classifier")

    try:
        parsed = json.loads(raw)
        return normalize_intent(parsed)
    except:
        return {
            "intent": "unknown",
            "metric": None,
            "dimension": None,
            "limit": None
        }