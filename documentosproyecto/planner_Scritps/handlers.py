'''from agents.sql_validator import validate_sql

MAX_ROWS = 1000


def handle_sql(step, context, connector, tool):

    query = step["input"]

    schema = connector.get_schema()
    columns = schema["column_name"].tolist()

    validate_sql(query, columns)

    result = tool.run(query, connector, context)

    if result is None:
        raise ValueError("SQL devolvió None")

    if len(result) == 0:
        raise ValueError("La consulta no devolvió resultados")

    if len(result) > MAX_ROWS:
        raise ValueError("Resultado demasiado grande")

    context["last_result"] = result


def handle_insight(step, context, connector, tool):

    if "last_result" not in context:
        raise ValueError("Insight sin datos")

    result = tool.run(
        step["input"],   # 🔥 SOLO string
        connector,
        context
    )

    context["explanation"] = result

    return result
'''