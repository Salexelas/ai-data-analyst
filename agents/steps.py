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
            llm=self.llm,
            language=ctx.language
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
                {
                    "last_result": ctx.result,
                    "language": ctx.language   # 👈 NUEVO
                }
            )
        except Exception as e:
            ctx.insight = f"Insight error: {str(e)}"


class DetectLanguageStep:
    name = "detect_language"

    def run(self, ctx):
        prompt = f"""
Detect the language of this text.

Text:
{ctx.question}

Return ONLY one code:
es, en, pt, de, fr, it
"""

        try:
            lang = ctx.llm.generate(
                prompt,
                system_prompt="You are a language detector"
            ).strip().lower()

            if lang not in ["es", "en", "pt", "de", "fr", "it"]:
                lang = "en"

        except:
            lang = "en"

        ctx.language = lang
        print("LANG DETECTED:", ctx.language)