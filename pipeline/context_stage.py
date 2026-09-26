from connectors.multi_connector import MultiDatasetConnector
from pipeline.query_context_factory import QueryContextFactory


def build_context(
    question,
    dataset_ids=None,
    dataset_relations=None,
    semantic_layer=None,
    inline_datasets=None,
    connector=None,  # 👈 Agregamos connector con valor por defecto
    llm=None,
    trace_id=None,
):
    # Si no viene un conector ya creado (ej: desde Slack legacy), lo instanciamos
    if connector is None:
        connector = MultiDatasetConnector(
            dataset_ids=dataset_ids or [],
            relations=dataset_relations or [],
            inline_datasets=inline_datasets,
        )

    return QueryContextFactory.create(
        question=question,
        connector=connector,
        semantic_layer=semantic_layer,
        llm=llm,
        trace_id=trace_id,
    )