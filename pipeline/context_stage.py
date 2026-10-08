from typing import Any, Optional
from core.dataset_store import DatasetStore


def build_context(
    question: str,
    dataset_id: str = None,
    dataset_ids: list[str] = None,
    dataset_relations: list[dict] = None,
    semantic_layer: dict = None,
    taxonomies: dict = None,
    examples: list = None,
    inline_datasets: dict = None,
    connector=None,
    llm=None,
    trace_id: str = None,
    **kwargs,
) -> dict:
    """Construye el contexto.

    Registra el YAML la primera vez y lo reutiliza de memoria en subsecuentes
    preguntas.
    """
    target_id = (
        dataset_id
        or (dataset_ids[0] if dataset_ids else None)
        or (semantic_layer.get("dataset_id") if semantic_layer else None)
    )

    # 1. Si enviaron el YAML completo en este request, registrarlo / actualizarlo en memoria
    if semantic_layer and "columns" in semantic_layer:
        d_id = semantic_layer.get("dataset_id", target_id)
        if d_id:
            DatasetStore.register(d_id, semantic_layer)
            target_id = d_id

    # 2. Si solo mandaron el ID (preguntas subsecuentes), recuperarlo del store
    elif target_id and DatasetStore.exists(target_id):
        semantic_layer = DatasetStore.get(target_id)

    else:
        semantic_layer = semantic_layer or {}

    # 3. Prioridad a los objetos enviados explícitamente, de lo contrario se leen de semantic_layer
    resolved_taxonomies = taxonomies or semantic_layer.get("taxonomies", {})
    resolved_examples = examples or semantic_layer.get("examples", [])

    return {
        "question": question,
        "trace_id": trace_id,
        "dataset_id": target_id,
        "dataset_ids": dataset_ids or ([target_id] if target_id else []),
        "dataset_relations": dataset_relations or [],
        "inline_datasets": inline_datasets or {},

        # NUEVO: conservar el schema del dataset
        "inline_dataset_schema": kwargs.get(
            "inline_dataset_schema",
            {},
        ),

        "llm": llm,
        "connector": connector,
        "semantic_layer": semantic_layer,
        "taxonomies": resolved_taxonomies,
        "examples": resolved_examples,
        "schema_columns": list(
            semantic_layer.get("columns", {}).keys()
        ),
    }