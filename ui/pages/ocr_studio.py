import streamlit as st
import os
from datetime import datetime

from services.ocr.loader import load_ocr
from services.ocr.llm_parser_service import OCRLLMParserService
from services.ocr.validator_service import OCRValidatorService
from connectors.factory import create_connector

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)


def render_ocr_studio():

    st.title("📷 OCR Studio")

    uploaded = st.file_uploader(
        "Subir archivo",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if not uploaded:
        return

    # limpiar estado si cambia archivo
    current_file = uploaded.name
    if st.session_state.get("ocr_last_file") != current_file:
        st.session_state["ocr_last_file"] = current_file
        st.session_state["ocr_raw_text"] = ""
        st.session_state.pop("ocr_df", None)

    # =========================
    # OCR
    # =========================
    if "ocr_raw_text" not in st.session_state:
        st.session_state["ocr_raw_text"] = ""

    if st.button("Leer archivo"):

        with st.spinner("Procesando OCR..."):

            ocr = load_ocr()

            # IMPORTANTE: pasar solo bytes
            text = ocr.extract_text(
                uploaded.getvalue()
            )

            st.session_state["ocr_raw_text"] = text

    # =========================
    # RAW TEXT
    # =========================
    if st.session_state["ocr_raw_text"]:

        st.subheader("Texto detectado (editable)")

        editable_text = st.text_area(
            "Corregí si hace falta",
            value=st.session_state["ocr_raw_text"],
            height=320
        )

        context = st.text_input(
            "Contexto",
            placeholder="Ej: factura ferretería / estadísticas NBA"
        )

        columns = st.text_input(
            "Columnas",
            placeholder="Ej: producto,cantidad,precio_unitario"
        )

        examples = st.text_area(
            "Ejemplos (opcional)",
            placeholder="Ej:\nPintura,3,15500\nCeramica,2,12000"
        )

        # =========================
        # GENERATE DATAFRAME
        # =========================
        if st.button("Generar dataset"):

            cols = [
                c.strip()
                for c in columns.split(",")
                if c.strip()
            ]

            if not cols:
                st.warning("Ingresá al menos una columna")
                return

            parser = OCRLLMParserService()

            with st.spinner("Estructurando dataset..."):

                df = parser.parse_to_dataframe(
                    raw_text=editable_text,
                    columns=cols,
                    examples=examples,
                    context=context,
                    llm=st.session_state["llm"]
                )

            st.session_state["ocr_df"] = df

    # =========================
    # PREVIEW
    # =========================
    if "ocr_df" in st.session_state:

        st.subheader("Preview dataset")

        edited_df = st.data_editor(
            st.session_state["ocr_df"],
            use_container_width=True,
            num_rows="dynamic"
        )

        validator = OCRValidatorService()

        errors = validator.validate_dataframe(
            edited_df
        )

        if errors:

            for err in errors:
                st.error(err)

        else:

            st.success("Dataset válido ✔")

            if st.button("Guardar dataset"):

                file_name = datetime.now().strftime(
                    "ocr_%Y%m%d_%H%M%S"
                ) + ".csv"

                save_path = os.path.join(
                    DATA_PATH,
                    file_name
                )

                edited_df.to_csv(
                    save_path,
                    index=False
                )

                connector = create_connector(
                    "csv",
                    {"file_path": save_path}
                )

                st.session_state["connector"] = connector
                st.session_state["file_path"] = save_path
                st.session_state["dataset_id"] = file_name

                st.success(
                    f"Dataset guardado: {file_name}"
                )

                st.rerun()