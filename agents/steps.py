from agents.filters import (
    is_valid_question_basic,
    is_question_related_fast,
    detect_language_fast
)
from agents.intent_detector import detect_intent
from core.observability import log_event
from agents.sql_retry import generate_sql_with_retry
from tools.insight_tool import InsightTool
from agents.sql_guard import guard_sql
from tools.insight_prompt_builder import build_insight_prompt
from tools.analytics_response_parser import parse_analytics_response


class IntentStep:
    name = "intent"

    def __init__(self, llm):
        self.llm = llm

    def run(self, ctx):
        intent = detect_intent(ctx.input.question, self.llm, ctx.input.semantic_layer)
        ctx.exec.intent = intent

        log_event(
            "intent_detected",
            ctx.trace_id,
            intent=intent
        )


class ValidateStep:
    name = "validate"

    def run(self, ctx):
        q = ctx.input.question

        if not is_valid_question_basic(q):
            raise ValueError("Pregunta inválida")

        if not is_question_related_fast(q, ctx.input.semantic_layer):
            print("⚠️ Low confidence question, continuing anyway")


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
        log_event("question", ctx.trace_id, question=ctx.input.question)
        ctx.exec.sql = generate_sql_with_retry(
            ctx.input.question,
            ctx.exec.schema,
            ctx.input.semantic_layer,
            ctx.exec.columns,
            llm=self.llm,
            language=ctx.exec.language,
            intent=ctx.exec.intent 
        )
        log_event("sql_generated", ctx.trace_id, sql=ctx.exec.sql)


class ExecuteSQLStep:
    name = "execute_sql"

    def run(self, ctx):
        safe_sql = guard_sql(ctx.exec.sql, ctx.exec.columns)
        log_event(
            "sql_execute",
            ctx.trace_id,
            sql=safe_sql
        )
        ctx.exec.safe_sql = safe_sql
        result = ctx.input.connector.execute(safe_sql)

        if result is None or len(result) == 0:
            raise ValueError("Sin resultados")

        ctx.output.result = result
        log_event(
            "sql_result",
            ctx.trace_id,
            rows=len(result)
        )

class InsightStep:

    name = "insight"

    def __init__(self, llm):
        self.llm = llm

    def run(self, ctx):

        try:

            df = ctx.output.result

            # -------------------------
            # GUARDS
            # -------------------------
            if df is None or len(df) == 0:

                ctx.output.markdown = "# ⚠️ Sin datos"

                ctx.output.metrics = {}

                ctx.output.chart_type = None

                ctx.output.severity = "warning"

                return

            # -------------------------
            # LIMIT
            # -------------------------
            if len(df) > 50:

                ctx.output.markdown = (
                    "# ⚠️ Resultado muy grande\n\n"
                    "El resultado contiene demasiadas filas para generar insights automáticos."
                )

                ctx.output.metrics = {}

                ctx.output.chart_type = None

                ctx.output.severity = "warning"

                return

            # -------------------------
            # DATA PREP
            # -------------------------
            df = df.round(2)

            preview = df.head(10).to_dict(orient="records")

            data = {
                "rows": preview,
                "intent": ctx.exec.intent.get("intent")
                if ctx.exec.intent else None
            }

            # -------------------------
            # PROMPT
            # -------------------------
            prompt = build_insight_prompt(
                ctx.input.question,
                data,
                ctx.exec.language
            )

            # -------------------------
            # GENERATE
            # -------------------------
            raw_response = self.llm.generate(
                prompt,
                system_prompt="""
You are a senior BI analyst.

Return ONLY valid JSON.

FORMAT:

{
    "markdown": "...",
    "chart_type": "...",
    "severity": "...",
    "metrics": {
        "kpi_1": "...",
        "kpi_2": "..."
    }
}

RULES:
- markdown must be executive style
- use headings
- use bullets
- use emojis
- concise
- no HTML
"""
            )

            # -------------------------
            # PARSE
            # -------------------------
            parsed = parse_analytics_response(raw_response)

            # -------------------------
            # OUTPUT
            # -------------------------
            ctx.output.markdown = parsed.get("markdown")

            ctx.output.chart_type = parsed.get("chart_type")

            ctx.output.metrics = parsed.get("metrics", {})

            ctx.output.severity = parsed.get("severity", "info")

            log_event(
                "insight_generated",
                ctx.trace_id,
                chart_type=ctx.output.chart_type,
                severity=ctx.output.severity
            )

        except Exception as e:

            ctx.output.markdown = (
                f"# ❌ Insight Error\n\n{str(e)}"
            )

            ctx.output.metrics = {}

            ctx.output.chart_type = None

            ctx.output.severity = "error"


class DetectLanguageStep:
    name = "detect_language"

    def run(self, ctx):
        ctx.exec.language = detect_language_fast(ctx.input.question)
        log_event("language_detected", ctx.trace_id, language=ctx.exec.language)

