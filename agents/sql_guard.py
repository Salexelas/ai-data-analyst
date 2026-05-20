import sqlglot
from sqlglot import exp

from core.settings import SQLConfig


def guard_sql(
    query: str,
    schema_columns: list,
    allowed_tables: list = None
) -> str:

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
    # TABLAS REALES
    # -------------------------
    if allowed_tables:

        used_tables = {
            t.name.lower()
            for t in parsed.find_all(exp.Table)
        }

        valid_tables = {
            t.lower()
            for t in allowed_tables
        }

        invalid_tables = used_tables - valid_tables

        if invalid_tables:
            raise ValueError(f"Tabla inválida: {invalid_tables}")

    # -------------------------
    # COLUMNAS
    # -------------------------
    used_columns = {
        c.name
        for c in parsed.find_all(exp.Column)
    }

    valid_columns = set(schema_columns)

    invalid = used_columns - valid_columns

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
    # LIMIT AUTO
    # -------------------------
    if not parsed.args.get("limit"):
        parsed.set(
            "limit",
            exp.Limit(
                expression=exp.Literal.number(
                    SQLConfig.MAX_ROWS
                )
            )
        )

    return parsed.sql()