from pipeline.context_stage import build_context
from pipeline.cache_stage import (
    get_cached_response,
    store_response,
)
from pipeline.execution_stage import (
    run_pre_pipeline,
    run_main_pipeline,
)
from core.observability import (
    new_trace_id,
)

from pipeline.error_handler import (
    ErrorHandler,
)


def answer_question(
    question,
    dataset_ids,
    dataset_relations=None,
    semantic_layer=None,
    llm=None,
):

    trace_id = new_trace_id()

    try:

        ctx = build_context(
            question,
            dataset_ids,
            dataset_relations,
            semantic_layer,
            llm,
            trace_id,
        )

        ctx = run_pre_pipeline(
            ctx,
            llm,
        )

        cached = get_cached_response(
            ctx,
            question,
            dataset_ids,
            semantic_layer,
            trace_id,
        )

        if cached:
            return cached

        response = run_main_pipeline(
            ctx,
            llm,
        )

        store_response(
            ctx,
            response,
        )

        return response

    except Exception as e:

        return ErrorHandler.to_response(e)