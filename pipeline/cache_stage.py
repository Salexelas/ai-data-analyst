from cache import (
    SimpleCache,
    build_cache_key,
)

cache = SimpleCache(ttl=300)

from core.observability import (
    log_event,
)


def get_cached_response(
    ctx,
    question,
    dataset_ids,
    semantic_layer,
    trace_id,
):

    cache_key = build_cache_key(
        question=question,
        dataset_id=sorted(dataset_ids),
        semantic_layer=semantic_layer,
        intent=ctx.exec.intent,
        language=ctx.exec.language,
    )

    ctx.cache_key = cache_key

    cached = cache.get(cache_key)

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

    return None


def store_response(
    ctx,
    response,
):

    cache.set(
        ctx.cache_key,
        response,
    )