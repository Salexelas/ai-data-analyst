import sqlglot
from sqlglot import exp

from core.settings import SQLConfig


def guard_sql(
    query: str,
    schema_columns: list[str],
    allowed_tables: list[str] | None = None,
) -> str:
    """
    Validate a SQL query before execution.
    """

    if not query:
        raise ValueError("Empty query")

    try:
        parsed = sqlglot.parse_one(query)
    except Exception as exc:
        raise ValueError("Invalid SQL") from exc

    if not isinstance(parsed, exp.Select):
        raise ValueError("Only SELECT statements are allowed")

    _validate_tables(parsed, allowed_tables)
    _validate_columns(parsed, schema_columns)
    _validate_joins(parsed)

    if not parsed.args.get("limit"):
        parsed.set(
            "limit",
            exp.Limit(
                expression=exp.Literal.number(SQLConfig.MAX_ROWS)
            ),
        )

    return parsed.sql()


def _validate_tables(
    parsed: exp.Expression,
    allowed_tables: list[str] | None,
) -> None:

    if not allowed_tables:
        return

    used_tables = {
        table.name.lower()
        for table in parsed.find_all(exp.Table)
    }

    invalid_tables = (
        used_tables
        - {table.lower() for table in allowed_tables}
    )

    if invalid_tables:
        raise ValueError(
            f"Invalid tables: {sorted(invalid_tables)}"
        )


def _validate_columns(
    parsed: exp.Expression,
    schema_columns: list[str],
) -> None:

    used_columns = {
        column.name
        for column in parsed.find_all(exp.Column)
    }

    invalid_columns = (
        used_columns
        - set(schema_columns)
    )

    if invalid_columns:
        raise ValueError(
            f"Invalid columns: {sorted(invalid_columns)}"
        )


def _validate_joins(
    parsed: exp.Expression,
) -> None:

    joins = list(parsed.find_all(exp.Join))

    if len(joins) > SQLConfig.MAX_JOINS:
        raise ValueError("Too many JOINs")

    if any(
        join.args.get("kind") == "cross"
        for join in joins
    ):
        raise ValueError(
            "CROSS JOIN is not allowed"
        )