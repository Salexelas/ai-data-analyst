class SQLGenerationStep:
    name = "generate_sql"

    def __init__(self, sql_service):
        self.sql_service = sql_service

    def run(self, ctx):

        ctx.exec.sql = self.sql_service.generate(ctx)

        return ctx