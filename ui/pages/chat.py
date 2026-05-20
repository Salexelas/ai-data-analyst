import os
import streamlit as st

from services.speech.loader import load_whisper
from agents.service import answer_question
from core.query_store import save_query

from ui.components.audio_input import render_audio_input
from renderers.streamlit_renderer import render_analytics

DATA_PATH = "data"


def switch_dataset(file_name: str):
    file_path = os.path.join(DATA_PATH, file_name)

    file_type = (
        "csv" if file_name.endswith(".csv")
        else "excel" if file_name.endswith(".xlsx")
        else None
    )

    if not file_type:
        return

    # mantener dataset activo para UI
    st.session_state["file_path"] = file_path
    st.session_state["dataset_id"] = file_name

    # multi selección
    if "active_datasets" not in st.session_state:
        st.session_state["active_datasets"] = []

    if file_name not in st.session_state["active_datasets"]:
        st.session_state["active_datasets"].append(file_name)


def remove_dataset(file_name: str):
    if "active_datasets" not in st.session_state:
        return

    if file_name in st.session_state["active_datasets"]:
        st.session_state["active_datasets"].remove(file_name)


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
            "Consulta sobre datasets",
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

        # ==========================================
        # DATASETS DISPONIBLES
        # ==========================================

        available_datasets = (
            sorted(os.listdir(DATA_PATH))
            if os.path.exists(DATA_PATH)
            else []
        )

        st.markdown("---")

        with st.expander("📚 Datasets disponibles", expanded=False):

            active = st.session_state.get(
                "active_datasets",
                []
            )

            for ds in available_datasets:

                col1, col2, col3 = st.columns([4, 1, 1])

                with col1:
                    st.write(ds)

                with col2:
                    if ds in active:
                        st.success("Activo")
                    else:
                        if st.button(
                            "Agregar",
                            key=f"add_{ds}"
                        ):
                            switch_dataset(ds)
                            st.rerun()

                with col3:
                    if ds in active:
                        if st.button(
                            "Quitar",
                            key=f"remove_{ds}"
                        ):
                            remove_dataset(ds)
                            st.rerun()

        # ==========================================
        # DATASETS ACTIVOS
        # ==========================================

        active = st.session_state.get(
            "active_datasets",
            []
        )

        if active:
            st.info(
                "Datasets activos: " + ", ".join(active)
            )
            # ==========================================
            # RELACIONES ENTRE DATASETS
            # ==========================================

            if len(active) >= 2:

                st.markdown("### 🔗 Relacionar datasets")

                if "dataset_relations" not in st.session_state:
                    st.session_state["dataset_relations"] = []

                selected_left = st.selectbox(
                    "Dataset izquierdo",
                    active,
                    key="rel_left_ds"
                )

                selected_right = st.selectbox(
                    "Dataset derecho",
                    [d for d in active if d != selected_left],
                    key="rel_right_ds"
                )

                # -------------------------
                # leer columnas reales
                # -------------------------
                import pandas as pd

                left_path = os.path.join(DATA_PATH, selected_left)
                right_path = os.path.join(DATA_PATH, selected_right)

                left_cols = pd.read_csv(left_path, nrows=1).columns.tolist()
                right_cols = pd.read_csv(right_path, nrows=1).columns.tolist()

                left_col = st.selectbox(
                    "Columna izquierda",
                    left_cols,
                    key="rel_left_col"
                )

                right_col = st.selectbox(
                    "Columna derecha",
                    right_cols,
                    key="rel_right_col"
                )

                if st.button("Agregar relación"):

                    relation = {
                        "left_dataset": selected_left,
                        "left_column": left_col,
                        "right_dataset": selected_right,
                        "right_column": right_col
                    }

                    st.session_state["dataset_relations"].append(
                        relation
                    )

                    st.success("Relación agregada")
                    st.rerun()

                # mostrar relaciones
                if st.session_state["dataset_relations"]:

                    st.markdown("### Relaciones activas")

                    for i, rel in enumerate(
                        st.session_state["dataset_relations"]
                    ):

                        st.write(
                            f"{rel['left_dataset']}.{rel['left_column']} "
                            f"↔ "
                            f"{rel['right_dataset']}.{rel['right_column']}"
                        )
        else:
            st.warning("No hay datasets seleccionados")

        st.markdown("---")

        col1, col2 = st.columns([1, 1])

        with col1:

            if st.button("Ejecutar"):

                if not active:
                    st.error(
                        "Seleccioná al menos un dataset"
                    )
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
                    dataset_id=",".join(active),
                    intent=None
                )

                with st.spinner("🧠 Analizando..."):

                    response = answer_question(
                        question=question,
                        dataset_ids=active,
                        dataset_relations=st.session_state.get("dataset_relations", []),
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

        response = st.session_state.get(
            "last_response"
        )

        if response:

            if hasattr(response, "type") and response.type == "error":
                st.error(response.markdown)

            else:
                render_analytics(response)

        else:
            st.info(
                "Todavía no ejecutaste ninguna consulta"
            )

    with tabs[1]:
        st.markdown("### 🔀 Comparar datasets")
        st.info(
            "Ahora podés seleccionar varios datasets en la pestaña Chat."
        )

    with tabs[2]:
        st.markdown("### 📈 Opciones de vista")
        st.checkbox("Modo compacto")
        st.checkbox("Mostrar insight")
        st.checkbox("Mostrar SQL")