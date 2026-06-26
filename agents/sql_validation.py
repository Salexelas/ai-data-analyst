from agents.sql_guard import (
    guard_sql,
)


def validate_sql(
    parsed,
    schema,
    columns,
):

    sql = parsed["sql"]

    if "select" not in sql.lower():
        raise ValueError(
            "SQL inválido"
        )

    if len(sql) < 10:
        raise ValueError(
            "SQL demasiado corto"
        )

    tables = (
        schema["table_name"]
        .unique()
        .tolist()
    )

    return guard_sql(
        sql,
        columns,
        allowed_tables=tables,
    )