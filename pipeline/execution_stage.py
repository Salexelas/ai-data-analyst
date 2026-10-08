import duckdb
import pandas as pd

from agents.filters import is_valid_question
from agents.sql_retry import generate_sql_with_retry


def run_pre_pipeline(ctx: dict, llm=None) -> dict:
    """Validación previa rápida de la entrada sin llamadas al LLM."""

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
    Ejecuta el SQL generado por el Agent sobre los datasets
    enviados por la aplicación consumidora.

    Reconstruye los tipos originales del DataFrame antes
    de registrarlo en DuckDB.
    """

    if not sql:
        raise ValueError(
            "No se recibió una consulta SQL."
        )

    if not inline_datasets:
        raise ValueError(
            "No se recibieron datasets inline."
        )

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

    # ---------------------------------------------------------
    # Convertir records a DataFrame
    # ---------------------------------------------------------

    if isinstance(records, pd.DataFrame):

        df = records.copy()

    elif isinstance(records, list):

        df = pd.DataFrame(records)


    else:

        raise TypeError(
            f"Formato no soportado para inline_datasets['{dataset_id}']: "
            f"{type(records).__name__}"
        )

    df = _restore_date_columns(df)
    
    # ---------------------------------------------------------
    # Restaurar tipos originales
    # ---------------------------------------------------------

    dataset_schema = (
        (inline_dataset_schema or {})
        .get(dataset_id)
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

    # ---------------------------------------------------------
    # Ejecutar SQL
    # ---------------------------------------------------------

    con = duckdb.connect()

    try:

        con.register(
            dataset_id,
            df,
        )

        result_df = con.execute(sql).df()

        return result_df

    finally:

        con.close()


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
    # 2. EJECUTAR SQL SOBRE LOS DATOS REALES
    # =========================================================

    result_df = _execute_inline_sql(
        sql=sql_query,
        inline_datasets=ctx.get("inline_datasets"),
        semantic_layer=ctx.get("semantic_layer"),
        inline_dataset_schema=ctx.get("inline_dataset_schema"),
    )

    # =========================================================
    # 3. CONVERTIR RESULTADOS A JSON-SERIALIZABLE
    # =========================================================

    result_data = result_df.to_dict(
        orient="records"
    )

    # =========================================================
    # 4. SEGUNDO LLM
    #
    # IMPORTANTE:
    # Ahora el LLM recibe LOS RESULTADOS.
    # =========================================================

    answer_prompt = f"""
Eres un asistente de datos.

Pregunta del usuario:
{ctx["question"]}

Resultados reales obtenidos de la consulta:
{result_data}

Responde directamente la pregunta del usuario utilizando
únicamente los resultados proporcionados.

No inventes información.

No expliques el SQL salvo que sea necesario.

No digas que el usuario debe ejecutar la consulta.

Si hay resultados, responde con la información encontrada.

Si no hay resultados, indícalo claramente.
"""

    answer = llm.generate(
        answer_prompt,
        system_prompt="You are a helpful data analyst.",
    )

    # =========================================================
    # 5. RESPUESTA FINAL
    # =========================================================

    return {
        "status": "success",
        "trace_id": ctx.get("trace_id"),
        "question": ctx["question"],
        "sql": sql_query,
        "data": result_data,
        "answer": answer,
    }