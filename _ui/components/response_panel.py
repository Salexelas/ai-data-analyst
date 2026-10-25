import streamlit as st

from renderers.streamlit_renderer import (
    render_analytics
)


def render_response_panel():

    response = (
        st.session_state.get(
            "last_response"
        )
    )

    if not response:

        st.info(
            "Ninguna consulta fue hecha todavia."
        )

        return

    if (
        hasattr(response, "type")
        and response.type == "error"
    ):

        st.error(
            response.markdown
        )

        return

    render_analytics(
        response
    )