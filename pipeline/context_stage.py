from connectors.multi_connector import (
    MultiDatasetConnector,
)

from pipeline.query_context_factory import (
    QueryContextFactory,
)


def build_context(
    question,
    dataset_ids,
    dataset_relations,
    semantic_layer,
    llm,
    trace_id,
):

    connector = MultiDatasetConnector(
        dataset_ids,
        relations=dataset_relations or [],
    )

    return QueryContextFactory.create(
        question=question,
        connector=connector,
        semantic_layer=semantic_layer,
        llm=llm,
        trace_id=trace_id,
    )