class ExecutionStep:
    name = "execute"

    def __init__(self, execution_service):
        self.execution_service = execution_service

    def run(self, ctx):

        safe_sql, result = (
            self.execution_service.execute(
                sql=ctx.exec.sql,
                columns=ctx.exec.columns,
                connector=ctx.input.connector
            )
        )

        ctx.exec.safe_sql = safe_sql
        ctx.output.result = result

        return ctx