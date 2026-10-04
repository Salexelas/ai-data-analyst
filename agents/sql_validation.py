from agents.sql_guard import guard_sql

def validate_sql(
    parsed: str | dict,
    schema_columns: list[str],
    allowed_tables: list[str] = None
) -> str:
    # 1. Proteger contra Ellipsis (...) o None
    if parsed is ... or parsed is None:
        raise ValueError("SQL inválido: No se recibió ninguna consulta (recibido Ellipsis/None).")

    # 2. Extraer el string SQL según el tipo
    if isinstance(parsed, dict):
        sql = parsed.get("sql", "")
    elif isinstance(parsed, str):
        sql = parsed
    else:
        sql = str(parsed)

    # 3. Validar que sea un string válido y no esté vacío
    sql_clean = sql.strip()

    if not sql_clean or "select" not in sql_clean.lower():
        raise ValueError("SQL inválido: Debe contener una instrucción SELECT.")

    if len(sql_clean) < 10:
        raise ValueError("SQL demasiado corto.")

    # 4. Guard de seguridad en el SQL
    return guard_sql(
        sql_clean,
        schema_columns,
        allowed_tables=allowed_tables,
    )