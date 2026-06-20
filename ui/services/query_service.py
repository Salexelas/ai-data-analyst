import streamlit as st

from agents.service import answer_question
from core.query_store import save_query


class QueryService:

    @staticmethod
    def execute(
        question: str,
        active_datasets: list[str],
        dataset_relations: list
    ):

        save_query(
            question=question,
            dataset_id=",".join(
                active_datasets
            ),
            intent=None
        )

        return answer_question(
            question=question,
            dataset_ids=active_datasets,
            dataset_relations=dataset_relations,
            semantic_layer=st.session_state.get(
                "semantic_layer"
            ),
            llm=st.session_state["llm"]
        )