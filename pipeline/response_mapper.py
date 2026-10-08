'''from core.responses import (
    AnalyticsResponse
)


class ResponseMapper:

    @staticmethod
    def from_context(
        ctx
    ):

        return AnalyticsResponse(
            type="analytics",
            markdown=ctx.output.markdown,
            data=ctx.output.result.copy(),
            sql=ctx.exec.safe_sql,
            chart_type=ctx.output.chart_type,
            language=ctx.exec.language,
            metrics=ctx.output.metrics,
            severity=ctx.output.severity,
        )'''