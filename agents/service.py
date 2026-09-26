from pipeline.context_stage import build_context
from pipeline.cache_stage import (
    get_cached_response,
    store_response,
)
from pipeline.execution_stage import (
    run_pre_pipeline,
    run_main_pipeline,
)
from core.observability import new_trace_id
from pipeline.error_handler import ErrorHandler
from core.llm_service import LLMService  # 👈 Fallback por defecto si no nos pasan cliente LLM


def answer_question(
    question: str,
    dataset_ids: list[str] = None,
    dataset_relations: list[dict] = None,
    semantic_layer: dict = None,
    inline_datasets: dict = None,
    llm=None,
    # Parámetros legacy (para no romper Streamlit/Slack antiguos si usan 'connector' o 'dataset_id' único)
    connector=None,
    dataset_id: str = None,
):
    """
    Entry point principal del AI Agent Service.
    Soporta consumo desde FastAPI (CRM/ERP), Streamlit UI y Slack.
    """
    trace_id = new_trace_id()

    # 1. Fallback automático para LLM
    if llm is None:
        llm = LLMService()

    # 2. Normalización de parámetros de entrada (retrocompatibilidad)
    if dataset_ids is None:
        if dataset_id:
            dataset_ids = [dataset_id]
        else:
            dataset_ids = []

    try:
        # 3. Construcción del contexto del pipeline
        ctx = build_context(
            question=question,
            dataset_ids=dataset_ids,
            dataset_relations=dataset_relations,
            semantic_layer=semantic_layer,
            inline_datasets=inline_datasets,
            connector=connector,
            llm=llm,
            trace_id=trace_id,
        )

        # 4. Pre-pipeline (ej. clasificación de intent / normalización)
        ctx = run_pre_pipeline(
            ctx,
            llm,
        )

        # 5. Capa de Cache
        cached = get_cached_response(
            ctx,
            question,
            dataset_ids,
            semantic_layer,
            trace_id,
        )

        if cached:
            return cached

        # 6. Ejecución del Pipeline Principal (SQL generation, execution, insights, charts)
        response = run_main_pipeline(
            ctx,
            llm,
        )

        # 7. Guardado en Cache
        store_response(
            ctx,
            response,
        )

        return response

    except Exception as e:
        return ErrorHandler.to_response(e)  