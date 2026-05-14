import streamlit as st

from services.speech.loader import load_whisper
from agents.service import answer_question
from core.query_store import save_query

from ui.components.audio_input import render_audio_input
from renderers.streamlit_renderer import render_analytics


def render_chat():

    st.title("💬 Nueva conversación")

    tabs = st.tabs([
        "💬 Chat",
        "🔀 Comparación",
        "📈 Vista"
    ])

    with tabs[0]:

        default_q = st.session_state.get(
            "prefill_question",
            ""
        )

        text_prompt = st.text_input(
            "Consulta sobre dataset",
            value=default_q
        )

        audio = render_audio_input()

        if "audio_prompt" not in st.session_state:
            st.session_state["audio_prompt"] = ""

        if audio and "bytes" in audio:

            with st.spinner("🎧 Transcribiendo..."):

                transcription = load_whisper().transcribe(
                    audio["bytes"]
                )

            st.session_state["audio_prompt"] = transcription

        if st.session_state["audio_prompt"]:

            st.info(
                f"🎤 {st.session_state['audio_prompt']}"
            )

        question = (
            text_prompt
            or st.session_state["audio_prompt"]
        )

        col1, col2 = st.columns([1, 1])

        with col1:

            if st.button("Ejecutar"):

                if "connector" not in st.session_state:

                    st.error("Primero cargá un dataset")
                    return

                if not question:

                    st.warning("Ingresá una pregunta")
                    return

                st.session_state.setdefault(
                    "recent_queries",
                    []
                )

                if question not in st.session_state["recent_queries"]:

                    st.session_state["recent_queries"].insert(
                        0,
                        question
                    )

                save_query(
                    question,
                    dataset_id=st.session_state.get(
                        "dataset_id"
                    ),
                    intent=None
                )

                with st.spinner("🧠 Analizando..."):

                    response = answer_question(
                        question=question,
                        connector=st.session_state["connector"],
                        dataset_id=st.session_state.get("dataset_id"),
                        semantic_layer=st.session_state.get("semantic_layer"),
                        llm=st.session_state["llm"]
                    )

                st.session_state["last_response"] = response

        with col2:

            if st.button("Limpiar"):

                st.session_state["prefill_question"] = ""
                st.session_state["audio_prompt"] = ""

                st.session_state.pop(
                    "last_response",
                    None
                )

        st.markdown("---")

        response = st.session_state.get("last_response")

        if response:

            if response.type == "error":
                st.error(response.message)
            else:
                render_analytics(response)

        else:
            st.info("Todavía no ejecutaste ninguna consulta")

    with tabs[1]:
        st.markdown("### 🔀 Comparar datasets")
        st.info("Próximamente 🚧")

    with tabs[2]:
        st.markdown("### 📈 Opciones de vista")
        st.checkbox("Modo compacto")
        st.checkbox("Mostrar insight")
        st.checkbox("Mostrar SQL")