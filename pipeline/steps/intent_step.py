class IntentStep:
    name = "intent"

    def __init__(self, intent_service):
        self.intent_service = intent_service

    def run(self, ctx):

        ctx.exec.intent = self.intent_service.detect(
            question=ctx.input.question,
            semantic_layer=ctx.input.semantic_layer
        )

        return ctx