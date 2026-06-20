from agents.sql_retry import generate_sql_with_retry
from core.observability import log_event


class SQLService:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, ctx):

        relationships = (
            ctx.input.connector
            .get_relationships()
        )

        sql = generate_sql_with_retry(
            question=ctx.input.question,
            schema=ctx.exec.schema,
            semantic_layer=ctx.input.semantic_layer,
            columns=ctx.exec.columns,
            llm=self.llm,
            language=ctx.exec.language,
            intent=ctx.exec.intent,
            relationships=relationships
        )

        log_event(
            "sql_generated",
            ctx.trace_id,
            sql=sql
        )

        return sql