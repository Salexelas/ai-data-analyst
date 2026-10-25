import streamlit as st
from services.speech.loader import (load_whisper)
from ui.components.audio_input import (render_audio_input)


def render_query_panel() -> str:

    default_question = (
        st.session_state.get(
            "prefill_question",
            ""
        )
    )

    question_input = st.text_input(
        "Haz preguntas sobre tus datos",
        value=default_question
    )

    audio = render_audio_input()

    st.session_state.setdefault(
        "audio_prompt",
        ""
    )

    if audio and "bytes" in audio:

        with st.spinner(
            "🎧 Transcribing..."
        ):

            transcription = (
                load_whisper()
                .transcribe(
                    audio["bytes"]
                )
            )

        st.session_state[
            "audio_prompt"
        ] = transcription

    if st.session_state["audio_prompt"]:

        st.info(
            st.session_state[
                "audio_prompt"
            ]
        )

    return (
        question_input
        or st.session_state["audio_prompt"]
    )