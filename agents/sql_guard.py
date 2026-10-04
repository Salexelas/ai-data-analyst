import sqlglot
from sqlglot import exp
from core.settings import SQLConfig


def guard_sql(
    query: str,
    schema_columns: list[str] | list[dict] | dict,
    allowed_tables: list[str] | list[dict] | None = None,
) -> str:
    """Validate a SQL query before execution."""

    if not query:
        raise ValueError("Empty query")

    try:
        parsed = sqlglot.parse_one(query)
    except Exception as exc:
        raise ValueError("Invalid SQL") from exc

    if not isinstance(parsed, exp.Select):
        raise ValueError("Only SELECT statements are allowed")

    # Normalizar entradas si provienen directamente del YAML
    norm_tables = _normalize_to_list(allowed_tables)
    norm_columns = _normalize_to_list(schema_columns)

    _validate_tables(parsed, norm_tables)
    _validate_columns(parsed, norm_columns)
    _validate_joins(parsed)

    if not parsed.args.get("limit"):
        parsed.set(
            "limit",
            exp.Limit(
                expression=exp.Literal.number(SQLConfig.MAX_ROWS)
            ),
        )

    return parsed.sql()


def _normalize_to_list(data) -> list[str]:
    """Soporta listas de strings, listas de diccionarios YAML o claves de dicts."""
    if not data:
        return []
    if isinstance(data, dict):
        # Si es un dict tipo {'columns': ['a', 'b']} o {'col1': {...}}
        return list(data.keys())
    if isinstance(data, list):
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                # Si en el YAML la columna es {'name': 'producto', 'type': 'str'}
                val = item.get("name") or item.get("column") or item.get("id")
                if val:
                    result.append(str(val))
        return result
    return []


def _validate_tables(
    parsed: exp.Expression,
    allowed_tables: list[str],
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
    if not schema_columns:
        return

    physical_columns = {
        str(column).lower()
        for column in schema_columns
    }

    # CTEs disponibles en el query.
    cte_scopes = _collect_cte_scopes(parsed)

    # Derived tables:
    # FROM (...) r
    derived_scopes = _collect_derived_scopes(parsed)

    invalid_columns = set()

    for column in parsed.find_all(exp.Column):
        name = column.name.lower()
        table = column.table.lower() if column.table else None

        # ---------------------------------------------------------
        # 1. Physical column
        # ---------------------------------------------------------
        if name in physical_columns:
            continue

        # ---------------------------------------------------------
        # 2. Column exposed by a derived table / CTE
        # ---------------------------------------------------------
        if table:
            if table in derived_scopes:
                if name in derived_scopes[table]:
                    continue

            if table in cte_scopes:
                if name in cte_scopes[table]:
                    continue

        # ---------------------------------------------------------
        # 3. SELECT alias
        # ---------------------------------------------------------
        if _is_valid_select_alias(column, parsed):
            continue

        invalid_columns.add(name)

    if invalid_columns:
        raise ValueError(
            f"Invalid columns: {sorted(invalid_columns)}"
        )


def _collect_derived_scopes(
    parsed: exp.Expression,
) -> dict[str, set[str]]:
    """
    Detecta:

        FROM (
            SELECT ...
        ) r

    y construye:

        {
            "r": {
                "Responsable",
                "cnt"
            }
        }
    """

    scopes = {}

    for subquery in parsed.find_all(exp.Subquery):
        alias = subquery.alias

        if not alias:
            continue

        inner = subquery.this

        if not isinstance(inner, exp.Select):
            continue

        output_columns = _get_select_output_columns(inner)

        scopes[alias.lower()] = output_columns

    return scopes


def _collect_cte_scopes(
    parsed: exp.Expression,
) -> dict[str, set[str]]:
    """
    Detecta:

        WITH counts AS (
            SELECT ...
        )

    y construye:

        {
            "counts": {
                "Responsable",
                "cnt"
            }
        }
    """

    scopes = {}

    for cte in parsed.find_all(exp.CTE):
        alias = cte.alias

        if not alias:
            continue

        inner = cte.this

        if not isinstance(inner, exp.Select):
            continue

        output_columns = _get_select_output_columns(inner)

        scopes[alias.lower()] = output_columns

    return scopes


def _get_select_output_columns(
    select: exp.Select,
) -> set[str]:
    """
    Devuelve los nombres de las columnas que expone
    un SELECT hacia su scope exterior.

    Ejemplo:

        SELECT
            "Responsable",
            COUNT(*) AS cnt

    devuelve:

        {
            "responsable",
            "cnt"
        }
    """

    output_columns = set()

    for expression in select.expressions:

        # SELECT ... AS alias
        if expression.alias:
            output_columns.add(
                expression.alias.lower()
            )
            continue

        # SELECT "Responsable"
        if isinstance(expression, exp.Column):
            output_columns.add(
                expression.name.lower()
            )
            continue

        # Otros casos donde SQLGlot puede conocer el nombre.
        name = expression.name

        if name:
            output_columns.add(
                name.lower()
            )

    return output_columns


def _is_valid_select_alias(
    column: exp.Column,
    parsed: exp.Expression,
) -> bool:
    """
    Permite aliases generados por el SELECT principal.

    Ejemplo:

        SELECT COUNT(*) AS diferencia
        FROM erp_tasks
        ORDER BY diferencia DESC

    'diferencia' no es una columna física,
    pero sí es un alias válido del SELECT.
    """

    if column.table:
        return False

    name = column.name.lower()

    # Buscar SELECTs que expongan ese alias.
    for select in parsed.find_all(exp.Select):
        for expression in select.expressions:
            if expression.alias:
                if expression.alias.lower() == name:
                    return True

    return False


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
        raise ValueError("CROSS JOIN is not allowed")