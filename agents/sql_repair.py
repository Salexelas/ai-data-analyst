import json


def repair_sql_generation(
    question,
    schema,
    semantic_layer,
    intent,
    relationships,
    previous_output,
    error,
    llm,
):

    fix_prompt = f"""
You generated an invalid SQL query.

Fix it using the error.

Context:
Question: {question}

Schema:
{schema}

Semantic Layer:
{semantic_layer}

Intent:
{intent}

Relationships:
{relationships}

Previous output:
{previous_output}

Error:
{error}

Rules:
- Keep same intent
- Use relationships if JOIN is needed
- Preserve entity granularity
- Do not invent columns
- Fix ONLY the error
- Return ONLY valid JSON

Format:
{{
  "sql": "SELECT ...",
  "confidence": 0.0-1.0
}}
"""

    raw = llm.generate(
        fix_prompt,
        system_prompt="You fix SQL queries",
    )

    if not raw or not raw.strip():
        raise ValueError(
            "Invalid JSON"
        )

    raw = (
        raw.strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    decoder = json.JSONDecoder()

    parsed, _ = (
        decoder.raw_decode(raw)
    )

    return parsed