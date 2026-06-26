from agents.sql_generator import (
    generate_sql_structured,
)

from agents.sql_repair import (
    repair_sql_generation,
)

from agents.sql_validation import (
    validate_sql,
)

from agents.sql_generator import (
    LLMOutputFormatError,
)


def should_retry(error: str):

    error = error.lower()

    retryable = [
        "invalid json",
        "missing 'sql'",
        "sql inválido",
        "columnas inválidas",
        "tabla inválida",
        "solo select",
        "demasiados joins",
        "expecting value",
        "invalid json: empty response",
    ]

    return any(
        x in error
        for x in retryable
    )


def generate_sql_with_retry(
    question,
    schema,
    semantic_layer,
    columns,
    llm,
    language="en",
    intent=None,
    relationships=None,
    max_retries=2,
):

    last_error = None
    previous_output = None

    for _ in range(
        max_retries + 1
    ):

        try:

            if previous_output is None:

                parsed = (
                    generate_sql_structured(
                        question=question,
                        schema=schema,
                        semantic_layer=semantic_layer,
                        llm=llm,
                        language=language,
                        intent=intent,
                        relationships=relationships,
                    )
                )

            else:

                parsed = (
                    repair_sql_generation(
                        question=question,
                        schema=schema,
                        semantic_layer=semantic_layer,
                        intent=intent,
                        relationships=relationships,
                        previous_output=previous_output,
                        error=last_error,
                        llm=llm,
                    )
                )

            return validate_sql(
                parsed,
                schema,
                columns,
            )

        except Exception as e:

            last_error = str(e)
            previous_output = parsed

            if not should_retry(
                last_error
            ):
                raise

    raise ValueError(
        f"Failed after retries: {last_error}"
    )