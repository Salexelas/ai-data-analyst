from agents.filters import (
    is_valid_question_basic,
    is_question_related_fast
)

from agents.sql_retry import generate_sql_with_retry
from tools.insight_tool import InsightTool


class ValidateStep:
    name = "validate"

    def run(self, ctx):
        q = ctx.input.question

        if not is_valid_question_basic(q):
            raise ValueError("Pregunta inválida")

        if not is_question_related_fast(q, ctx.input.semantic_layer):
            raise ValueError("Pregunta no relacionada con los datos")


class LoadSchemaStep:
    name = "load_schema"

    def run(self, ctx):
        schema = ctx.input.connector.get_schema()
        ctx.exec.schema = schema
        ctx.exec.columns = schema["column_name"].tolist()


class GenerateSQLStep:
    name = "generate_sql"

    def __init__(self, llm):
        self.llm = llm

    def run(self, ctx):
        ctx.exec.sql = generate_sql_with_retry(
            ctx.input.question,
            ctx.exec.schema,
            ctx.input.semantic_layer,
            ctx.exec.columns,
            llm=self.llm,
            language=ctx.exec.language
        )


class ExecuteSQLStep:
    name = "execute_sql"

    def run(self, ctx):
        result = ctx.input.connector.execute(ctx.exec.sql)

        if result is None or len(result) == 0:
            raise ValueError("Sin resultados")

        ctx.output.result = result


class InsightStep:
    name = "insight"

    def __init__(self, llm):
        self.llm = llm

    def run(self, ctx):
        try:
            ctx.output.insight = InsightTool(self.llm).run(
                ctx.input.question,
                {
                    "last_result": ctx.output.result,
                    "language": ctx.exec.language
                }
            )
        except Exception as e:
            ctx.output.insight = f"Insight error: {str(e)}"


class DetectLanguageStep:
    name = "detect_language"

    def run(self, ctx):
        prompt = f"""
Detect the language of this text.

Text:
{ctx.input.question}

Return ONLY one code:
es, en, pt, de, fr, it
"""

        try:
            lang = ctx.input.llm.generate(
                prompt,
                system_prompt="You are a language detector"
            ).strip().lower()

            if lang not in ["es", "en", "pt", "de", "fr", "it"]:
                lang = "en"

        except:
            lang = "en"

        ctx.exec.language = lang
        print("LANG DETECTED:", ctx.exec.language)