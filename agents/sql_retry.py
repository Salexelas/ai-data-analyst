#from core.llm_service import LLMService
from agents.sql_generator import generate_sql
from agents.sql_validator import validate_sql
from agents.sql_cleaner import extract_sql


def should_retry(error: str):
    error = error.lower()

    if "columnas inválidas" in error:
        return True
    if "sql inválido" in error:
        return True

    return False


def generate_sql_with_retry(
    question,
    schema,
    semantic_layer,
    columns,
    llm,
    language="en",
    max_retries=1
):

    last_error = None
    sql = None

    for attempt in range(max_retries + 1):

        # -------------------------
        # 1. Primera generación
        # -------------------------
        if attempt == 0:
            raw = generate_sql(question, schema, semantic_layer, llm, language)
            print("RAW SQL:", raw)
            sql = extract_sql(raw)
            print("CLEAN SQL:", sql)

        # -------------------------
        # 2. Retry inteligente
        # -------------------------
        else:
            if not should_retry(last_error):
                raise ValueError(last_error)

            prompt = f"""
The following SQL failed:

{sql}

Error:
{last_error}

Fix the SQL.

Rules:
- Only SELECT
- Table name is data
- Use only these columns: {columns}
- No explanation
"""

            sql = llm.generate(
                prompt,
                system_prompt="You are a senior data engineer fixing SQL"
            )

        # -------------------------
        # 3. Validación
        # -------------------------
        try:
            validate_sql(sql, columns)
            return sql

        except Exception as e:
            last_error = str(e)

    raise ValueError(f"No se pudo generar SQL válido: {last_error}")