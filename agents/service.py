from typing import Union

from pipeline.context_stage import build_context
from pipeline.execution_stage import (
    run_pre_pipeline,
    run_main_pipeline,
)
from core.observability import new_trace_id
from core.llm_service import LLMService


def answer_question(
    question: str,
    dataset_ids: list[str] = None,
    dataset_relations: list[dict] = None,
    semantic_layer: dict = None,
    taxonomies: dict = None,
    examples: Union[list[dict], dict] = None,
    inline_datasets: dict = None,
    inline_dataset_schema: dict = None,
    llm=None,
    # Parámetros legacy
    connector=None,
    dataset_id: str = None,
    **kwargs,
):
    """
    Entry point principal del AI Agent Service.
    Soporta consumo desde FastAPI, Streamlit y Slack.
    """

    trace_id = new_trace_id()

    if llm is None:
        llm = LLMService()

    if dataset_ids is None:
        if dataset_id:
            dataset_ids = [dataset_id]
        else:
            dataset_ids = []

    try:

        ctx = build_context(
            question=question,
            dataset_ids=dataset_ids,
            dataset_relations=dataset_relations,
            semantic_layer=semantic_layer,
            taxonomies=taxonomies,
            examples=examples,
            inline_datasets=inline_datasets,
            inline_dataset_schema=inline_dataset_schema,
            connector=connector,
            llm=llm,
            trace_id=trace_id,
        )

        ctx = run_pre_pipeline(
            ctx,
            llm,
        )

        response = run_main_pipeline(
            ctx,
            llm,
        )

        return response

    except Exception:
        print("\n" + "=" * 80)
        print("ERROR REAL EN answer_question")
        print("=" * 80)

        import traceback
        traceback.print_exc()

        print("=" * 80 + "\n")

        raise