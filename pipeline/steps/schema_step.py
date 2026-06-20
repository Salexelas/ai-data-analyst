class SchemaStep:
    name = "schema"

    def __init__(self, schema_service):
        self.schema_service = schema_service

    def run(self, ctx):

        schema, columns = self.schema_service.load(
            ctx.input.connector
        )

        ctx.exec.schema = schema
        ctx.exec.columns = columns

        return ctx