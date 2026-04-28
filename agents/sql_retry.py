from agents.sql_generator import generate_sql_structured
from agents.sql_guard import guard_sql
from agents.sql_generator import LLMOutputFormatError


def should_retry(error: str):
    error = error.lower()

    retryable = [
        "invalid json",
        "missing 'sql'",
        "sql inválido",
        "columnas inválidas"
    ]

    return any(x in error for x in retryable)


def generate_sql_with_retry(
    question,
    schema,
    semantic_layer,
    columns,
    llm,
    language="en",
    max_retries=2
):

    last_error = None

    for attempt in range(max_retries + 1):

        try:
            # 🔥 generación estructurada
            parsed = generate_sql_structured(
                question,
                schema,
                semantic_layer,
                llm,
                language
            )

            sql = parsed["sql"]

            # 🔥 validación dura
            sql = guard_sql(sql, columns)

            return sql

        except Exception as e:

            last_error = str(e)

            if not should_retry(last_error):
                raise

            # 🔁 retry con contexto (SIN parsear texto)
            fix_prompt = f"""
Your previous output was invalid.

Error:
{last_error}

Fix it.

Return ONLY valid JSON:

{{
  "sql": "SELECT ...",
  "confidence": 0.0-1.0
}}
"""

            llm.generate(
                fix_prompt,
                system_prompt="Fix JSON output. No explanation."
            )

    raise ValueError(f"Failed after retries: {last_error}")