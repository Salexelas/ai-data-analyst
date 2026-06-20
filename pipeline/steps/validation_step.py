class ValidationStep:
    name = "validate"

    def __init__(self, validation_service):
        self.validation_service = validation_service

    def run(self, ctx):

        self.validation_service.validate(
            question=ctx.input.question,
            semantic_layer=ctx.input.semantic_layer
        )

        return ctx