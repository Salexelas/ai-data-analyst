import duckdb
import pandas as pd
import json

from agents.filters import is_valid_question
from agents.sql_retry import generate_sql_with_retry


def run_pre_pipeline(ctx: dict, llm=None) -> dict:
    """Validación previa sin llamadas al LLM."""

    if not is_valid_question(ctx["question"]):
        raise ValueError(
            "La pregunta no es válida o es demasiado corta."
        )

    ctx["intent"] = None
    return ctx


def _restore_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    for column in result.columns:
        series = result[column]

        if series.dtype != "object":
            continue

        values = series.dropna()

        if values.empty:
            continue

        converted = pd.to_datetime(
            values,
            errors="coerce",
        )

        if converted.notna().all():
            result[column] = pd.to_datetime(
                series,
                errors="coerce",
            )

    return result


def _execute_inline_sql(
    sql: str,
    inline_datasets: dict,
    semantic_layer: dict,
    inline_dataset_schema: dict = None,
) -> pd.DataFrame:
    """
    Ejecuta el SQL sobre los datos enviados por la aplicación
    consumidora y restaura los tipos declarados en su esquema.
    """

    if not sql:
        raise ValueError("No se recibió una consulta SQL.")

    if not inline_datasets:
        raise ValueError("No se recibieron datasets inline.")

    dataset_id = semantic_layer.get("dataset_id")

    if not dataset_id:
        raise ValueError(
            "El semantic layer no contiene 'dataset_id'."
        )

    records = inline_datasets.get(dataset_id)

    if records is None and len(inline_datasets) == 1:
        records = next(iter(inline_datasets.values()))

    if records is None:
        raise ValueError(
            f"No se encontró el dataset '{dataset_id}' "
            "en inline_datasets."
        )

    if isinstance(records, pd.DataFrame):
        df = records.copy()

    elif isinstance(records, list):
        df = pd.DataFrame(records)

    else:
        raise TypeError(
            f"Formato no soportado para inline_datasets"
            f"['{dataset_id}']: {type(records).__name__}"
        )

    df = _restore_date_columns(df)

    dataset_schema = (
        (inline_dataset_schema or {}).get(dataset_id)
    )

    if dataset_schema:
        for column, dtype in dataset_schema.items():

            if column not in df.columns:
                continue

            if dtype.startswith("datetime64"):
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce",
                )

            elif dtype == "date":
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce",
                ).dt.date

            elif dtype.startswith("int"):
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce",
                ).astype("Int64")

            elif dtype.startswith("float"):
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce",
                ).astype("Float64")

            elif dtype in ("bool", "boolean"):
                df[column] = df[column].astype("boolean")

            elif dtype in ("string", "object"):
                df[column] = df[column].astype("string")

    con = duckdb.connect()

    try:
        con.register(dataset_id, df)
        return con.execute(sql).df()

    finally:
        con.close()


def _normalize_chart(
    chart,
    result_df: pd.DataFrame,
):
    """
    Valida la especificación del gráfico sin conocer
    nombres concretos de datasets ni de sus columnas.

    Normaliza y a una lista para permitir múltiples series.
    La selección de series adicionales corresponde al
    componente de visualización del consumidor.
    """

    if not isinstance(chart, dict) or result_df.empty:
        return None

    allowed_chart_types = {"line", "bar", "scatter"}

    chart_type = chart.get("type")
    x = chart.get("x")
    y = chart.get("y")
    color = chart.get("color")

    columns = result_df.columns.tolist()

    # Compatibilidad con respuestas antiguas del LLM.
    if isinstance(y, str):
        y_columns = [y]

    elif isinstance(y, list):
        y_columns = y

    else:
        return None

    if not (
        chart_type in allowed_chart_types
        and isinstance(x, str)
        and x in columns
        and len(y_columns) > 0
        and all(
            isinstance(column, str)
            and column in columns
            and column != x
            for column in y_columns
        )
        and len(set(y_columns)) == len(y_columns)
        and (
            color is None
            or (
                isinstance(color, str)
                and color in columns
            )
        )
    ):
        return None

    return {
        "type": chart_type,
        "x": x,
        "y": y_columns,
        "title": str(
            chart.get("title") or "Análisis de datos"
        ),
        "color": color,
    }


def run_main_pipeline(ctx: dict, llm) -> dict:

    # =========================================================
    # 1. GENERAR SQL
    # =========================================================

    sql_query = generate_sql_with_retry(
        question=ctx["question"],
        schema_columns=ctx["schema_columns"],
        semantic_layer=ctx["semantic_layer"],
        llm=llm,
        taxonomies=ctx.get("taxonomies"),
        examples=ctx.get("examples"),
        intent=ctx.get("intent"),
    )

    if isinstance(sql_query, dict):
        sql_query = sql_query.get("sql", "")

    if not sql_query:
        raise ValueError(
            "El Agent no generó una consulta SQL válida."
        )

    ctx["generated_sql"] = sql_query

    # =========================================================
    # 2. EJECUTAR SQL
    # =========================================================

    result_df = _execute_inline_sql(
        sql=sql_query,
        inline_datasets=ctx.get("inline_datasets"),
        semantic_layer=ctx.get("semantic_layer"),
        inline_dataset_schema=ctx.get("inline_dataset_schema"),
    )

    # =========================================================
    # 3. SERIALIZAR RESULTADOS
    # =========================================================

    result_data = result_df.to_dict(orient="records")
    columns = result_df.columns.tolist()

    # =========================================================
    # 4. GENERAR RESPUESTA, INSIGHTS Y PROPUESTA DE GRÁFICO
    # =========================================================

    analytics_prompt = f"""
Eres un analista de datos que interpreta resultados SQL.

PREGUNTA:
{ctx["question"]}

COLUMNAS DISPONIBLES:
{json.dumps(columns, ensure_ascii=False)}

RESULTADOS REALES:
{json.dumps(result_data, ensure_ascii=False, default=str)}

TAREA:
1. Responder directamente la pregunta.
2. Identificar insights útiles respaldados por los resultados.
3. Proponer un gráfico solo si ayuda a comprender los resultados.

REGLAS:
- Usa exclusivamente los resultados proporcionados.
- No inventes datos, tendencias ni causas.
- No calcules porcentajes sin respaldo en los resultados.
- No confundas correlación con causalidad.
- Si hay un único resultado puntual, normalmente no propongas un gráfico.
- Si no hay resultados, devuelve insights vacíos y chart null.
- Usa únicamente nombres de columnas disponibles.
- No generes SQL, Python ni código para gráficos.
- Responde en español.
- Devuelve únicamente JSON válido, sin Markdown.

GRÁFICOS PERMITIDOS:
- line: evolución temporal o secuencial.
- bar: comparación de categorías o series.
- scatter: relación entre variables numéricas.

SELECCIÓN DE SERIES:
- "x" debe contener una columna de categorías o secuencia.
- "y" debe ser una LISTA de todas las columnas numéricas
  relevantes que se quieran comparar.
- Para comparaciones entre varias métricas, incluye todas
  las métricas relevantes en "y", no solamente la primera.
- Para una serie única, "y" también debe ser una lista
  con un solo elemento.
- No incluyas en "y" la columna seleccionada para "x".
- "color" es opcional y debe ser null o una columna
  disponible que represente una categoría.
- No inventes columnas ni valores.
- Si ninguna visualización ayuda a responder, usa chart null.

FORMATO OBLIGATORIO:
{{
    "answer": "Respuesta directa",
    "insights": [
        "Insight respaldado por los resultados"
    ],
    "chart": {{
        "type": "bar",
        "x": "nombre_columna",
        "y": ["metrica_1", "metrica_2"],
        "title": "Título del gráfico",
        "color": null
    }}
}}

Si no corresponde mostrar un gráfico, devuelve "chart": null.
Si no hay insights útiles, devuelve "insights": [].
"""

    raw_analytics = llm.generate(
        analytics_prompt,
        system_prompt=(
            "You are a data analyst. "
            "Return only valid JSON matching the requested schema."
        ),
    )

    # =========================================================
    # 5. PARSEAR RESPUESTA
    # =========================================================

    try:
        raw = str(raw_analytics).strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "", 1)
            raw = raw.replace("```", "").strip()

        analytics = json.loads(raw)

        if not isinstance(analytics, dict):
            raise ValueError(
                "La respuesta no es un objeto JSON."
            )

    except (json.JSONDecodeError, ValueError, TypeError):
        analytics = {
            "answer": str(raw_analytics),
            "insights": [],
            "chart": None,
        }

    answer = analytics.get("answer", "")

    if not isinstance(answer, str):
        answer = ""

    insights = analytics.get("insights", [])

    if not isinstance(insights, list):
        insights = []

    insights = [
        item.strip()
        for item in insights
        if isinstance(item, str) and item.strip()
    ]

    # =========================================================
    # 6. VALIDAR Y NORMALIZAR GRÁFICO
    # =========================================================

    chart = _normalize_chart(
        analytics.get("chart"),
        result_df,
    )

    # =========================================================
    # 7. RESPUESTA FINAL DE LA API
    # =========================================================

    # Definimos los pasos del pipeline que se enviarán a la UI
    pipeline_steps = [
        {"step": "schema", "label": "Carga de Esquema", "status": "success"},
        {"step": "intent", "label": "Detección de Intención", "status": "success"},
        {"step": "generate_sql", "label": "Generación SQL (Retry)", "status": "success"},
        {"step": "validate", "label": "Validación SQL Guard", "status": "success"},
        {"step": "execute", "label": "Ejecución en DuckDB", "status": "success"},
        {"step": "insight", "label": "Generación de Insights y Gráfico", "status": "success"}
    ]

    return {
        "status": "success",
        "trace_id": ctx.get("trace_id"),
        "question": ctx["question"],
        "sql": sql_query,
        "data": result_data,
        "answer": answer,
        "insights": insights,
        "chart": chart,
        "pipeline_flow": pipeline_steps  # <-- NUEVO: Se expone para que la app (components.py) lo consuma
    }
