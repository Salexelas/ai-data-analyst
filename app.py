import streamlit as st

from ui.components.sidebar import render_sidebar

from core.session_manager import initialize_session
from core.startup_service import autoload_last_dataset
from router.routes import ROUTES

st.set_page_config(layout="wide")


def main():

    initialize_session()
    autoload_last_dataset()

    render_sidebar()

    page = st.session_state.get("page", "chat")
    ROUTES.get(page, ROUTES["chat"])()


if __name__ == "__main__":
    main()