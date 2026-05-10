import streamlit as st

from agents.service import answer_question
from core.query_store import save_query

from ui.components.audio_input import (
    render_audio_input
)

# 🔥 NUEVO
from renderers.streamlit_renderer import (
    render_analytics
)


def render_chat():

    st.title("💬 Nueva conversación")

    tabs = st.tabs([
        "💬 Chat",
        "🔀 Comparación",
        "📈 Vista"
    ])

    # =========================
    # TAB CHAT
    # =========================
    with tabs[0]:

        default_q = st.session_state.get(
            "prefill_question",
            ""
        )

        # =========================
        # 🔹 INPUT TEXTO
        # =========================
        text_prompt = st.text_input(
            "Escribí tu pregunta...",
            value=default_q
        )

        # =========================
        # 🔹 AUDIO
        # =========================
        audio = render_audio_input()

        # =========================
        # INIT
        # =========================
        if "audio_prompt" not in st.session_state:

            st.session_state["audio_prompt"] = ""

        # =========================
        # TRANSCRIBE
        # =========================
        if audio and "bytes" in audio:

            with st.spinner("🎧 Transcribiendo..."):

                transcription = (
                    st.session_state["whisper"]
                    .transcribe(audio["bytes"])
                )

            st.session_state[
                "audio_prompt"
            ] = transcription

        # =========================
        # SHOW AUDIO
        # =========================
        if st.session_state["audio_prompt"]:

            st.info(
                f"🎤 {st.session_state['audio_prompt']}"
            )

        # =========================
        # FINAL QUESTION
        # =========================
        question = (
            text_prompt
            or st.session_state["audio_prompt"]
        )

        # =========================
        # BUTTONS
        # =========================
        col1, col2 = st.columns([1, 1])

        # =========================
        # EXECUTE
        # =========================
        with col1:

            if st.button("Ejecutar"):

                # -------------------------
                # DATASET VALIDATION
                # -------------------------
                if "connector" not in st.session_state:

                    st.error(
                        "Primero cargá un dataset"
                    )

                    return

                # -------------------------
                # QUESTION VALIDATION
                # -------------------------
                if not question:

                    st.warning(
                        "Ingresá una pregunta"
                    )

                    return

                # -------------------------
                # RECENTS
                # -------------------------
                st.session_state.setdefault(
                    "recent_queries",
                    []
                )

                if (
                    question
                    not in st.session_state[
                        "recent_queries"
                    ]
                ):

                    st.session_state[
                        "recent_queries"
                    ].insert(
                        0,
                        question
                    )

                # -------------------------
                # SAVE QUERY
                # -------------------------
                save_query(
                    question,
                    dataset_id=st.session_state.get(
                        "dataset_id"
                    ),
                    intent=None
                )

                # -------------------------
                # PIPELINE
                # -------------------------
                with st.spinner(
                    "🧠 Analizando..."
                ):

                    response = answer_question(

                        question=question,

                        connector=st.session_state[
                            "connector"
                        ],

                        dataset_id=st.session_state.get(
                            "dataset_id"
                        ),

                        semantic_layer=st.session_state.get(
                            "semantic_layer"
                        ),

                        llm=st.session_state[
                            "llm"
                        ]
                    )

                st.session_state[
                    "last_response"
                ] = response

        # =========================
        # CLEAR
        # =========================
        with col2:

            if st.button("Limpiar"):

                st.session_state[
                    "prefill_question"
                ] = ""

                st.session_state[
                    "audio_prompt"
                ] = ""

                st.session_state.pop(
                    "last_response",
                    None
                )

        st.markdown("---")

        # =========================
        # RESULT
        # =========================
        response = st.session_state.get(
            "last_response"
        )

        if response:

            # -------------------------
            # ERROR
            # -------------------------
            if response.type == "error":

                st.error(
                    response.message
                )

            # -------------------------
            # ANALYTICS RESPONSE
            # -------------------------
            else:

                render_analytics(response)

        else:

            st.info(
                "Todavía no ejecutaste ninguna consulta"
            )

    # =========================
    # TAB COMPARACIÓN
    # =========================
    with tabs[1]:

        st.markdown(
            "### 🔀 Comparar datasets"
        )

        st.info(
            "Próximamente 🚧"
        )

    # =========================
    # TAB VISTA
    # =========================
    with tabs[2]:

        st.markdown(
            "### 📈 Opciones de vista"
        )

        st.checkbox(
            "Modo compacto"
        )

        st.checkbox(
            "Mostrar insight"
        )

        st.checkbox(
            "Mostrar SQL"
        )