from core.observability import (
    new_trace_id,
    log_event,
)

from cache import (
    SimpleCache,
    build_cache_key,
)

from connectors.multi_connector import (
    MultiDatasetConnector,
)

from pipeline.pipeline_factory import (
    PipelineFactory,
)

from pipeline.query_context_factory import (
    QueryContextFactory,
)

from pipeline.response_mapper import (
    ResponseMapper,
)

from pipeline.error_handler import (
    ErrorHandler,
)

cache = SimpleCache(ttl=300)


def answer_question(
    question,
    dataset_ids,
    dataset_relations=None,
    semantic_layer=None,
    llm=None,
):

    trace_id = new_trace_id()

    connector = MultiDatasetConnector(
        dataset_ids,
        relations=dataset_relations or [],
    )

    ctx = QueryContextFactory.create(
        question=question,
        connector=connector,
        semantic_layer=semantic_layer,
        llm=llm,
        trace_id=trace_id,
    )

    log_event(
        "request_start",
        trace_id,
        question=question,
    )

    # -------------------------
    # PRE PIPELINE
    # -------------------------

    pre_pipeline = (
        PipelineFactory.build_pre_pipeline(
            llm
        )
    )

    ctx = pre_pipeline.run(ctx)

    # -------------------------
    # CACHE
    # -------------------------

    cache_key = build_cache_key(
        question=question,
        dataset_id=sorted(dataset_ids),
        semantic_layer=semantic_layer,
        intent=ctx.exec.intent,
        language=ctx.exec.language,
    )

    cached = cache.get(
        cache_key
    )

    if cached:

        log_event(
            "cache_hit",
            trace_id,
            key=cache_key,
        )

        return cached

    log_event(
        "cache_miss",
        trace_id,
        key=cache_key,
    )

    # -------------------------
    # MAIN PIPELINE
    # -------------------------

    try:

        pipeline = (
            PipelineFactory.build_main_pipeline(
                llm
            )
        )

        ctx = pipeline.run(
            ctx
        )

        log_event(
            "request_success",
            trace_id,
            rows=(
                len(ctx.output.result)
                if ctx.output.result is not None
                else 0
            ),
        )

        response = (
            ResponseMapper
            .from_context(ctx)
        )

        cache.set(
            cache_key,
            response,
        )

        log_event(
            "cache_set",
            trace_id,
            key=cache_key,
        )

        return response

    except Exception as e:

        log_event(
            "request_error",
            trace_id,
            error=str(e),
        )

        return (
            ErrorHandler
            .to_response(e)
        )