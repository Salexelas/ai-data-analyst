from core.query_context import QueryContext, InputContext
from core.pipeline import Pipeline
from agents.steps import *

from core.observability import new_trace_id, log_event
from core.responses import AnalyticsResponse

from cache import SimpleCache, build_cache_key
from connectors.multi_connector import MultiDatasetConnector


cache = SimpleCache(ttl=300)


def answer_question(
    question,
    dataset_ids,
    dataset_relations=None,
    semantic_layer=None,
    llm=None
):

    trace_id = new_trace_id()

    # =========================
    # MULTI DATASET CONNECTOR
    # =========================
    connector = MultiDatasetConnector(
        dataset_ids,
        relations=dataset_relations or []
    )

    ctx = QueryContext(
        input=InputContext(
            question=question,
            connector=connector,
            semantic_layer=semantic_layer,
            llm=llm
        ),
        trace_id=trace_id
    )

    log_event(
        "request_start",
        trace_id,
        question=question
    )

    # =========================
    # PRE PIPELINE
    # =========================
    pre_pipeline = Pipeline([
        ValidateStep(),
        DetectLanguageStep(),
        IntentStep(llm),
    ])

    ctx = pre_pipeline.run(ctx)

    # =========================
    # CACHE
    # =========================
    cache_key = build_cache_key(
        question=question,
        dataset_id=sorted(dataset_ids),
        semantic_layer=semantic_layer,
        intent=ctx.exec.intent,
        language=ctx.exec.language
    )

    cached = cache.get(cache_key)

    if cached:
        log_event("cache_hit", trace_id, key=cache_key)
        return cached

    log_event("cache_miss", trace_id, key=cache_key)

    # =========================
    # MAIN PIPELINE
    # =========================
    pipeline = Pipeline([
        LoadSchemaStep(),
        GenerateSQLStep(llm),
        ExecuteSQLStep(),
        InsightStep(llm)
    ])

    try:

        ctx = pipeline.run(ctx)

        log_event(
            "request_success",
            trace_id,
            rows=len(ctx.output.result)
            if ctx.output.result is not None else 0
        )

        response = AnalyticsResponse(
            type="analytics",
            markdown=ctx.output.markdown,
            data=ctx.output.result.copy(),
            sql=ctx.exec.safe_sql,
            chart_type=ctx.output.chart_type,
            language=ctx.exec.language,
            metrics=ctx.output.metrics,
            severity=ctx.output.severity
        )

        cache.set(cache_key, response)

        log_event(
            "cache_set",
            trace_id,
            key=cache_key
        )

        return response

    except Exception as e:

        log_event(
            "request_error",
            trace_id,
            error=str(e)
        )

        error_msg = str(e).lower()

        print("ERROR:", error_msg)

        if any(x in error_msg for x in [
            "sin resultados",
            "columnas inválidas",
            "sql inválido",
            "tabla inválida"
        ]):
            return AnalyticsResponse(
                type="table",
                data=[],
                markdown="No encontré resultados claros. Probá reformular la pregunta."
            )

        return AnalyticsResponse(
            type="error",
            data=[],
            markdown=f"Error: {str(e)}"
        )