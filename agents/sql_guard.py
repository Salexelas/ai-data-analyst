import sqlglot
from sqlglot import exp

from core.settings import SQLConfig
from core.constants import ALLOWED_TABLE


def guard_sql(query: str, schema_columns: list) -> str:

    if not query:
        raise ValueError("Empty query")

    # -------------------------
    # Parse
    # -------------------------
    try:
        parsed = sqlglot.parse_one(query)
    except Exception:
        raise ValueError("SQL inválido")

    # -------------------------
    # SOLO SELECT
    # -------------------------
    if not isinstance(parsed, exp.Select):
        raise ValueError("Solo SELECT permitido")

    # -------------------------
    # TABLA
    # -------------------------
    tables = {t.name for t in parsed.find_all(exp.Table)}
    if tables != {ALLOWED_TABLE}:
        raise ValueError("Tabla inválida")

    # -------------------------
    # COLUMNAS
    # -------------------------
    used_columns = {c.name for c in parsed.find_all(exp.Column)}
    invalid = used_columns - set(schema_columns)

    if invalid:
        raise ValueError(f"Columnas inválidas: {invalid}")

    # -------------------------
    # JOIN CONTROL
    # -------------------------
    join_count = 0

    for join in parsed.find_all(exp.Join):
        join_count += 1

        if join.args.get("kind") == "cross":
            raise ValueError("CROSS JOIN no permitido")

    if join_count > SQLConfig.MAX_JOINS:
        raise ValueError("Demasiados JOINs")

    # -------------------------
    # LIMIT FORZADO
    # -------------------------
    if not parsed.args.get("limit"):
        parsed.set(
            "limit",
            exp.Limit(expression=exp.Literal.number(SQLConfig.MAX_ROWS))
        )

    return parsed.sql()