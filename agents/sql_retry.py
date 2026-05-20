import json
from agents.sql_generator import generate_sql_structured
from agents.sql_guard import guard_sql
from agents.sql_generator import LLMOutputFormatError


def should_retry(error: str):
    error = error.lower()

    retryable = [
        "invalid json",
        "missing 'sql'",
        "sql inválido",
        "columnas inválidas",
        "tabla inválida",
        "solo select",
        "demasiados joins",
        "expecting value",
        "invalid json: empty response"
    ]

    return any(x in error for x in retryable)


def generate_sql_with_retry(
    question,
    schema,
    semantic_layer,
    columns,
    llm,
    language="en",
    intent=None,
    relationships=None,
    max_retries=2
):

    last_error = None
    previous_output = None

    for attempt in range(max_retries + 1):

        try:

            # -------------------------
            # 1. GENERACIÓN
            # -------------------------
            if previous_output is None:

                parsed = generate_sql_structured(
                    question=question,
                    schema=schema,
                    semantic_layer=semantic_layer,
                    llm=llm,
                    language=language,
                    intent=intent,
                    relationships=relationships
                )

            else:
                # 🔥 FIX INTELIGENTE (CON CONTEXTO REAL)
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
{last_error}

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
                    system_prompt="You fix SQL queries"
                )

                raw = raw.strip()

                if not raw:
                    raise ValueError("Invalid JSON")

                raw = raw.replace("```json", "").replace("```", "").strip()

                decoder = json.JSONDecoder()
                parsed, _ = decoder.raw_decode(raw)

            # -------------------------
            # 2. EXTRAER SQL
            # -------------------------
            sql = parsed["sql"]

            # -------------------------
            # 3. VALIDACIÓN LIVIANA
            # -------------------------
            if "select" not in sql.lower():
                raise ValueError("SQL inválido")

            if len(sql) < 10:
                raise ValueError("SQL demasiado corto")

            # -------------------------
            # 4. 🔥 GUARD DENTRO DEL RETRY
            # -------------------------
            tables = schema["table_name"].unique().tolist()

            print("\nTABLAS DISPONIBLES:")
            print(tables)

            print("\nSQL GENERADO:")
            print(sql)

            safe_sql = guard_sql(
                sql,
                columns,
                allowed_tables=tables
            )

            # ✅ si pasa el guard, terminamos
            return safe_sql

        except Exception as e:

            last_error = str(e)

            # 👇 MUY IMPORTANTE: guardar salida previa SI existe
            previous_output = parsed if 'parsed' in locals() else None

            if not should_retry(last_error):
                raise

    raise ValueError(f"Failed after retries: {last_error}")