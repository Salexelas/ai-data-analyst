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


def _execute_inline_sql(
    sql: str,
    inline_datasets: dict,
    semantic_layer: dict,
) -> pd.DataFrame:
    """
    Ejecuta el SQL generado por el Agent sobre los datasets
    enviados por la aplicación consumidora.

    La aplicación consumidora NO necesita DuckDB.
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

    # ---------------------------------------------------------
    # El ERP puede enviar:
    #
    # inline_datasets = {
    #     "tareas_filtradas": [...]
    # }
    #
    # mientras que semantic_layer tiene:
    #
    # dataset_id: erp_tasks
    #
    # El SQL generado utiliza erp_tasks.
    # ---------------------------------------------------------

    records = inline_datasets.get(dataset_id)

    # Si el nombre enviado por el consumidor no coincide con
    # dataset_id, pero solamente hay un dataset, usamos ese.
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

        df = records

    elif isinstance(records, list):

        df = pd.DataFrame(records)

    else:

        raise TypeError(
            f"Formato no soportado para inline_datasets['{dataset_id}']: "
            f"{type(records).__name__}"
        )

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