from core.query_context import (
    QueryContext,
    InputContext,
)


class QueryContextFactory:

    @staticmethod
    def create(
        question,
        connector,
        semantic_layer,
        llm,
        trace_id,
    ):

        return QueryContext(
            input=InputContext(
                question=question,
                connector=connector,
                semantic_layer=semantic_layer,
                llm=llm,
            ),
            trace_id=trace_id,
        )