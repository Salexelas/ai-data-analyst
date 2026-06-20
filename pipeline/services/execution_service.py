from agents.sql_guard import guard_sql


class ExecutionService:

    def execute(
        self,
        sql,
        columns,
        connector
    ):

        safe_sql = guard_sql(
            sql,
            columns
        )

        result = connector.execute(
            safe_sql
        )

        if result is None:
            raise ValueError(
                "No results returned"
            )

        if len(result) == 0:
            raise ValueError(
                "Empty result"
            )

        return safe_sql, result