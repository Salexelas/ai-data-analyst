'''from core.llm_service import LLMService


def generate_sql(question, schema, semantic_layer, llm, language="en"):

    semantic_text = ""

    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases: {semantic_layer.get("aliases")}
Metrics: {semantic_layer.get("metrics")}
"""

    prompt = f"""
Generate a SQL query.

Rules:
- Only SELECT
- Table name is data
- Use correct columns
- No explanation

INTENT HANDLING:
- "top" → ORDER BY DESC
- "bottom" → ORDER BY ASC
- "average" → use AVG()
- "total" → use SUM()

AMBIGUITY:
- If multiple matches (e.g. "Los Angeles"), return all matches using LIKE


Schema:
{schema}

{semantic_text}

Question:
{question}
"""

    return llm.generate(
        prompt,
        system_prompt=f"You are a senior data analyst. The user speaks {language}",
        trace_id=getattr(llm, "trace_id", None)
    )'''



import json


class LLMOutputFormatError(Exception):
    pass


def build_prompt(question, schema, semantic_layer, language="en"):

    semantic_text = ""
    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases: {semantic_layer.get("aliases")}
Metrics: {semantic_layer.get("metrics")}
"""

    return f"""
Return ONLY valid JSON.

Format:
{{
  "sql": "string",
  "confidence": float
}}

Rules:
- Only SELECT
- Table name is data
- Use correct columns
- No explanation
- No markdown

INTENT:
- "top" → ORDER BY DESC
- "bottom" → ORDER BY ASC
- "average" → AVG()
- "total" → SUM()

Schema:
{schema}

{semantic_text}

Question:
{question}
"""


def validate_llm_output(parsed):
    if not isinstance(parsed, dict):
        raise LLMOutputFormatError("Output is not a JSON object")

    if "sql" not in parsed:
        raise LLMOutputFormatError("Missing 'sql' field")

    if not isinstance(parsed["sql"], str):
        raise LLMOutputFormatError("SQL must be string")

    if "confidence" in parsed and not isinstance(parsed["confidence"], (int, float)):
        raise LLMOutputFormatError("Confidence must be numeric")


def generate_sql_structured(question, schema, semantic_layer, llm, language="en"):

    prompt = build_prompt(question, schema, semantic_layer, language)

    raw = llm.generate(
        prompt,
        system_prompt="You are a senior data analyst. Output ONLY valid JSON.",
        trace_id=getattr(llm, "trace_id", None)
    )

    try:
        parsed = json.loads(raw)
    except Exception:
        raise LLMOutputFormatError("Invalid JSON")

    if not isinstance(parsed, dict):
        raise LLMOutputFormatError("Output is not a JSON object")

    if "sql" not in parsed:
        raise LLMOutputFormatError("Missing 'sql'")

    return parsed