from agents.filters import (
    is_valid_question_basic,
    is_question_related_fast
)

from agents.sql_retry import generate_sql_with_retry
from tools.insight_tool import InsightTool


class ValidateStep:
    name = "validate"

    def run(self, ctx):
        if not is_valid_question_basic(ctx.question):
            raise ValueError("Pregunta inválida")

        if not is_question_related_fast(ctx.question, ctx.semantic_layer):
            raise ValueError("Pregunta no relacionada con los datos")


class LoadSchemaStep:
    name = "load_schema"

    def run(self, ctx):
        schema = ctx.connector.get_schema()
        ctx.schema = schema
        ctx.columns = schema["column_name"].tolist()


class GenerateSQLStep:
    name = "generate_sql"

    def __init__(self, llm):
        self.llm = llm

    def run(self, ctx):
        ctx.sql = generate_sql_with_retry(
            ctx.question,
            ctx.schema,
            ctx.semantic_layer,
            ctx.columns,
            llm=self.llm
        )


class ExecuteSQLStep:
    name = "execute_sql"

    def run(self, ctx):
        result = ctx.connector.execute(ctx.sql)

        if result is None or len(result) == 0:
            raise ValueError("Sin resultados")

        ctx.result = result


class InsightStep:
    name = "insight"

    def __init__(self, llm):
        self.llm = llm

    def run(self, ctx):
        try:
            ctx.insight = InsightTool(self.llm).run(
                ctx.question,
                {"last_result": ctx.result}
            )
        except Exception as e:
            ctx.insight = f"Insight error: {str(e)}"