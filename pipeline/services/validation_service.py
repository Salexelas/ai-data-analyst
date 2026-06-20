from agents.filters import (
    is_valid_question_basic,
    is_question_related_fast
)


class ValidationService:

    def validate(
        self,
        question,
        semantic_layer
    ):

        if not is_valid_question_basic(question):
            raise ValueError("Invalid question")

        if not is_question_related_fast(
            question,
            semantic_layer
        ):
            print(
                "⚠️ Low confidence question, continuing anyway"
            )