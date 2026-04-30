from core.query_context import QueryContext, InputContext
from core.pipeline import Pipeline
from agents.steps import *
from core.observability import new_trace_id, log_event

# 🔥 NUEVO
from cache import SimpleCache, build_cache_key

cache = SimpleCache(ttl=300)


def answer_question(question, connector, dataset_id=None, semantic_layer=None, llm=None):

    trace_id = new_trace_id()

    ctx = QueryContext(
        input=InputContext(
            question=question,
            connector=connector,
            semantic_layer=semantic_layer,
            llm=llm
        ),
        trace_id=trace_id
    )

    log_event("request_start", trace_id, question=question)

    # -------------------------
    # 🔥 PIPELINE PARCIAL (ANTES DEL CACHE)
    # -------------------------
    pre_pipeline = Pipeline([
        ValidateStep(),
        DetectLanguageStep(),
        IntentStep(llm),
    ])

    ctx = pre_pipeline.run(ctx)

    # -------------------------
    # 🔥 CACHE (AHORA SÍ BIEN)
    # -------------------------
    cache_key = build_cache_key(
        question,
        dataset_id,
        semantic_layer,
        ctx.exec.intent,
        ctx.exec.language
    )

    cached = cache.get(cache_key)

    if cached:
        log_event("cache_hit", trace_id, key=cache_key)
        return cached

    log_event("cache_miss", trace_id, key=cache_key)

    # -------------------------
    # RESTO PIPELINE
    # -------------------------
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
            rows=len(ctx.output.result) if ctx.output.result is not None else 0
        )

        # ⚠️ IMPORTANTE → copiar DF
        response = {
            "type": "table",
            "data": ctx.output.result.copy(),
            "explanation": ctx.output.insight,
            "language": ctx.exec.language
        }

        # -------------------------
        # 🔥 GUARDAR CACHE
        # -------------------------
        cache.set(cache_key, response)
        log_event("cache_set", trace_id, key=cache_key)

        return response

    except Exception as e:

        log_event("request_error", trace_id, error=str(e))

        error_msg = str(e).lower()
        print("❌ ERROR:", error_msg)

        if any(x in error_msg for x in [
            "sin resultados",
            "columnas inválidas",
            "sql inválido"
        ]):
            return {
                "type": "table",
                "data": [],
                "explanation": "No encontré resultados claros. Probá reformular la pregunta.",
                "language": "es"
            }

        return {
            "type": "error",
            "message": str(e)
        }