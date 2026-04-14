import sqlglot

ALLOWED_TABLE = "data"


def validate_sql(query: str, schema_columns: list):

    try:
        parsed = sqlglot.parse_one(query)
    except Exception:
        raise ValueError("SQL inválido")

    if parsed.key != "select":
        raise ValueError("Solo SELECT permitido")

    tables = {t.name for t in parsed.find_all(sqlglot.exp.Table)}
    if tables != {ALLOWED_TABLE}:
        raise ValueError("Tabla inválida")

    used_columns = {c.name for c in parsed.find_all(sqlglot.exp.Column)}

    invalid = used_columns - set(schema_columns)

    if invalid:
        raise ValueError(f"Columnas inválidas: {invalid}")

    return True