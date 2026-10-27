'''from tools.insight_prompt_builder import (
    build_insight_prompt
)

from tools.analytics_response_parser import (
    parse_analytics_response
)


class InsightService:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, ctx):

        try:

            df = ctx.output.result

            if df is None or len(df) == 0:

                ctx.output.markdown = (
                    "# ⚠️ No data"
                )

                ctx.output.metrics = {}
                ctx.output.chart_type = None
                ctx.output.severity = "warning"

                return

            df = df.round(2)

            preview = (
                df.head(10)
                .to_dict(
                    orient="records"
                )
            )

            data = {
                "rows": preview,
                "intent":
                    ctx.exec.intent.get(
                        "intent"
                    )
                    if ctx.exec.intent
                    else None
            }

            prompt = build_insight_prompt(
                ctx.input.question,
                data,
                ctx.exec.language
            )

            response = (
                self.llm.generate(
                    prompt,
                    system_prompt=
                    "You are a senior BI analyst. Return ONLY valid JSON."
                )
            )

            parsed = (
                parse_analytics_response(
                    response
                )
            )

            ctx.output.markdown = (
                parsed.get(
                    "markdown"
                )
            )

            ctx.output.chart_type = (
                parsed.get(
                    "chart_type"
                )
            )

            ctx.output.metrics = (
                parsed.get(
                    "metrics",
                    {}
                )
            )

            ctx.output.severity = (
                parsed.get(
                    "severity",
                    "info"
                )
            )

        except Exception as e:

            ctx.output.markdown = (
                f"# ❌ Insight Error\n\n{e}"
            )

            ctx.output.metrics = {}
            ctx.output.chart_type = None
            ctx.output.severity = "error"'''