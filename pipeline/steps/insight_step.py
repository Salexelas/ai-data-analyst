class InsightStep:
    name = "insight"

    def __init__(self, insight_service):
        self.insight_service = insight_service

    def run(self, ctx):

        self.insight_service.generate(ctx)

        return ctx