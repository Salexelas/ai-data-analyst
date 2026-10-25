import streamlit as st
from ui.services.query_service import QueryService
from ui.components.query_panel import render_query_panel
from ui.components.dataset_panel import render_dataset_panel
from ui.components.relationship_panel import render_relationship_panel
from ui.components.response_panel import render_response_panel

def render_chat():

    st.title(
        "💬 New Conversation"
    )

    question = (
        render_query_panel()
    )

    st.markdown("---")

    render_dataset_panel()

    render_relationship_panel()

    st.markdown("---")

    if st.button("Ejecutar"):

        active_datasets = (
            st.session_state.get(
                "active_datasets",
                []
            )
        )

        if not active_datasets:

            st.error(
                "Select at least one dataset."
            )

            return

        if not question:

            st.warning(
                "Enter a question."
            )

            return

        with st.spinner(
            "🧠 Analyzing..."
        ):

            response = (
                QueryService.execute(
                    question=question,
                    active_datasets=active_datasets,
                    dataset_relations=st.session_state.get(
                        "dataset_relations",
                        []
                    )
                )
            )

        st.session_state[
            "last_response"
        ] = response

    render_response_panel()