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
                ctx.output.insight = "No hay datos."
                return

            if len(df) > 50:
                ctx.output.insight = "Resultado grande — insight omitido por performance."
                return

            # -------------------------
            # DATA PREP (🔥 clave)
            # -------------------------
            df = df.round(2)

            preview = df.head(10).to_dict(orient="records")

            data = {
                "rows": preview,
                "intent": ctx.exec.intent.get("intent") if ctx.exec.intent else None
            }

            # -------------------------
            # 1. GENERATE
            # -------------------------
            prompt = build_insight_prompt(
                ctx.input.question,
                data,
                ctx.exec.language
            )

            raw_insight = self.llm.generate(
                prompt,
                system_prompt="You are a precise data analyst"
            )

            # -------------------------
            # 2. SELF-CHECK (🔥 FIX REAL)
            # -------------------------
            check_prompt = f"""
You are a senior data analyst.

Rewrite the following analysis so that:

- ALL numeric comparisons are correct
- NO contradictions exist
- The result is a CLEAN INSIGHT (not a validation report)

STRICT RULES:
- Do NOT explain errors
- Do NOT mention validation
- Do NOT list checks
- ONLY output the final insight
- Keep it concise and readable
- Focus on key differences and relevant comparisons

DATA:
{data}

TEXT:
{raw_insight}
"""

            final_insight = self.llm.generate(
                check_prompt,
                system_prompt="You validate and rewrite analytical insights"
            )

            ctx.output.insight = final_insight.strip()

        except Exception as e:
            ctx.output.insight = f"Insight error: {str(e)}"


class DetectLanguageStep:
    name = "detect_language"

    def run(self, ctx):
        ctx.exec.language = detect_language_fast(ctx.input.question)
        log_event("language_detected", ctx.trace_id, language=ctx.exec.language)

