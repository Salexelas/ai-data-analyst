from agents.sql_generator import (
    generate_sql_structured,
)
from agents.sql_repair import repair_sql_generation
from agents.sql_validation import validate_sql


def should_retry(error: str) -> bool:
    error_lower = error.lower()

    retryable_patterns = [
        "json",
        "missing 'sql'",
        "invalid sql",
        "column",
        "table",
        "select",
    ]

    return any(
        pattern in error_lower
        for pattern in retryable_patterns
    )


def generate_sql_with_retry(
    question: str,
    schema_columns: list[str],
    semantic_layer: dict,
    llm,
    taxonomies: dict = None,
    examples: list = None,
    intent: dict = None,
    max_retries: int = 2,
) -> str:

    last_error = None
    previous_output = None

    # ---------------------------------------------------------
    # Tabla permitida
    # ---------------------------------------------------------

    dataset_id = (
        semantic_layer.get("dataset_id")
        if isinstance(semantic_layer, dict)
        else None
    )

    allowed_tables = (
        [dataset_id]
        if dataset_id
        else None
    )

    # ---------------------------------------------------------
    # Retry loop
    # ---------------------------------------------------------

    for attempt in range(max_retries + 1):

        parsed = None

        try:

            # =================================================
            # Primera generación
            # =================================================

            if previous_output is None:

                parsed = generate_sql_structured(
                    question=question,
                    semantic_layer=semantic_layer,
                    llm=llm,
                    taxonomies=taxonomies,
                    examples=examples,
                    intent=intent,
                )
                print("\n" + "=" * 80)
                print("SQL GENERATION DEBUG")
                print("=" * 80)
                print("QUESTION:")
                print(question)
                print("\nPARSED OUTPUT:")
                print(parsed)
                print("=" * 80 + "\n")

            # =================================================
            # Reparación
            # =================================================

            else:

                parsed = repair_sql_generation(
                    question=question,
                    schema=schema_columns,
                    semantic_layer=semantic_layer,
                    intent=intent,
                    previous_output=previous_output,
                    error=last_error,
                    llm=llm,
                )

            # =================================================
            # Validación
            # =================================================

            return validate_sql(
                parsed=parsed,
                schema_columns=schema_columns,
                allowed_tables=allowed_tables,
            )

        except Exception as e:

            last_error = str(e)

            # Guardar la salida anterior si existe
            if parsed is not None and parsed is not ...:
                previous_output = parsed

            # Si el error no es recuperable, salir inmediatamente
            if not should_retry(last_error):
                raise

    raise ValueError(
        f"Fallo tras {max_retries} reintentos. "
        f"Último error: {last_error}"
    )