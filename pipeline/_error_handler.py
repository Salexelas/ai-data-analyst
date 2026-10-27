'''from core.responses import (
    AnalyticsResponse
)


class ErrorHandler:

    NO_RESULT_ERRORS = [
        "sin resultados",
        "columnas inválidas",
        "sql inválido",
        "tabla inválida",
        "empty result",
        "no results returned",
    ]

    @classmethod
    def to_response(
        cls,
        exception,
    ):

        error_message = (
            str(exception)
            .lower()
        )

        if any(
            error in error_message
            for error in cls.NO_RESULT_ERRORS
        ):

            return AnalyticsResponse(
                type="table",
                data=[],
                markdown=(
                    "No encontré resultados claros. "
                    "Probá reformular la pregunta."
                ),
            )

        return AnalyticsResponse(
            type="error",
            data=[],
            markdown=f"Error: {exception}",
        )'''