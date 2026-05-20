import json


class LLMOutputFormatError(Exception):
    pass


def build_prompt(
    question,
    schema,
    semantic_layer,
    intent=None,
    language="en",
    relationships=None
):

    available_tables = ", ".join(
        schema["table_name"].unique()
    )

    intent_text = ""
    if intent:
        intent_text = f"""
Intent:
Type: {intent.get("intent")}
Metric: {intent.get("metric")}
Dimension: {intent.get("dimension")}
Limit: {intent.get("limit")}
"""

    semantic_text = ""
    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases: {semantic_layer.get("aliases")}
Metrics: {semantic_layer.get("metrics")}
Columns: {semantic_layer.get("columns")}
"""

    relationships_text = ""
    if relationships:
        relationships_text = f"""
Relationships:
{json.dumps(relationships, indent=2)}

IMPORTANT:
- Use these relationships when JOIN is required.
- Preserve requested entity granularity.
- If relation is one_to_many or many_to_many, aggregate after JOIN.
- Avoid duplicated rows.
- Never duplicate entities due to JOIN.
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
- Use ONLY columns from schema
- No explanation
- No markdown
- Respect intent
- Use JOIN only when necessary

INTENT:
- top -> ORDER BY DESC
- bottom -> ORDER BY ASC
- average -> AVG()
- total -> SUM()

Available tables:
{available_tables}

{intent_text}

Schema:
{schema.to_dict(orient="records")}

{semantic_text}

{relationships_text}

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


def generate_sql_structured(
    question,
    schema,
    semantic_layer,
    llm,
    language="en",
    intent=None,
    relationships=None
):

    prompt = build_prompt(
        question=question,
        schema=schema,
        semantic_layer=semantic_layer,
        intent=intent,
        language=language,
        relationships=relationships
    )

    raw = llm.generate(
        prompt,
        system_prompt="You are a senior data analyst. Return ONLY valid JSON."
    )

    if not raw or not raw.strip():
        raise LLMOutputFormatError("Invalid JSON: empty response")

    raw = raw.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        decoder = json.JSONDecoder()
        parsed, _ = decoder.raw_decode(raw)

    except Exception:
        print("LLM RAW RESPONSE:")
        print(raw)
        raise LLMOutputFormatError(f"Invalid JSON: {raw}")

    validate_llm_output(parsed)

    return parsed