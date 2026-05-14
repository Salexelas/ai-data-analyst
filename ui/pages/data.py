import streamlit as st
import os
import pandas as pd
import json

from datetime import datetime

from connectors.factory import create_connector
from semantic.utils import get_dataset_id, load_semantic_layer

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)


def render_data():

    st.title("📥 Gestión de Datos")

    tabs = st.tabs([
        "📂 Subir archivo",
        "🔗 Conectar fuente",
        "📊 Preview"
    ])

    # ==================================================
    # TAB 1
    # ==================================================
    with tabs[0]:

        # -----------------------------------------
        # CSV / EXCEL
        # -----------------------------------------
        st.subheader("📂 Subir Dataset")

        file = st.file_uploader(
            "Subir CSV / Excel",
            type=["csv", "xlsx"]
        )

        if file and st.button("Cargar archivo"):

            file_path = os.path.join(
                DATA_PATH,
                file.name
            )

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

            file_type = (
                "csv"
                if file.name.endswith(".csv")
                else "excel"
            )

            connector = create_connector(
                file_type,
                {"file_path": file_path}
            )

            st.session_state["connector"] = connector
            st.session_state["file_path"] = file_path

            dataset_id = get_dataset_id(
                file_type,
                {"file": file.name}
            )

            st.session_state["dataset_id"] = dataset_id

            loaded = load_semantic_layer(dataset_id)

            if loaded:
                st.session_state["semantic_layer"] = loaded

            st.success(f"✅ Dataset guardado en {file_path}")

        st.markdown("---")

        # -----------------------------------------
        # OCR IMAGE
        # -----------------------------------------
        st.subheader("📷 Cargar imagen")

        image_file = st.file_uploader(
            "Subir imagen",
            type=["png", "jpg", "jpeg"],
            key="ocr_upload"
        )

        if image_file and st.button("Procesar imagen"):

            with st.spinner("Leyendo imagen..."):

                text = st.session_state["ocr"].extract_text(
                    image_file.getvalue()
                )

            st.session_state["ocr_text"] = text

        # -----------------------------------------
        # OCR TEXT
        # -----------------------------------------
        if "ocr_text" in st.session_state:

            st.text_area(
                "Texto detectado",
                st.session_state["ocr_text"],
                height=250
            )

            instruction = st.text_input(
                "Indicá qué columnas querés extraer",
                placeholder="Ej: producto, cantidad, precio"
            )

            if instruction and st.button("Generar dataset"):

                with st.spinner("Generando dataset..."):

                    ocr_text = st.session_state["ocr_text"]

                    prompt = f"""
Sos un parser de OCR.

Convertí este texto en un JSON array válido.

Reglas:
- usar exactamente las columnas pedidas
- si falta un valor dejar null
- no inventar datos
- devolver SOLO JSON
- sin markdown
- sin explicación
- todas las filas posibles

Texto OCR:
{ocr_text}

Columnas solicitadas:
{instruction}

Ejemplo salida:
[
  {{"producto":"A","cantidad":2,"precio":100}}
]
"""

                    response = st.session_state["llm"].generate(
                        prompt=prompt,
                        system_prompt="Convert OCR text to structured JSON"
                    )

                    response = response.strip()
                    response = response.replace("```json", "")
                    response = response.replace("```", "")
                    response = response.strip()

                    try:

                        data = json.loads(response)

                        df = pd.DataFrame(data)

                        st.session_state["ocr_df"] = df

                        st.success("✅ Dataset generado")

                    except Exception as e:

                        st.error(f"Error parseando respuesta: {e}")
                        st.code(response)

        # -----------------------------------------
        # SHOW DATAFRAME
        # -----------------------------------------
        if "ocr_df" in st.session_state:

            st.subheader("📊 Dataset generado")

            edited_df = st.data_editor(
                st.session_state["ocr_df"],
                use_container_width=True,
                num_rows="dynamic"
            )

            if st.button("Guardar dataset OCR"):

                file_name = datetime.now().strftime(
                    "ocr_%Y%m%d_%H%M%S"
                ) + ".csv"

                file_path = os.path.join(
                    DATA_PATH,
                    file_name
                )

                edited_df.to_csv(
                    file_path,
                    index=False
                )

                connector = create_connector(
                    "csv",
                    {"file_path": file_path}
                )

                st.session_state["connector"] = connector
                st.session_state["file_path"] = file_path
                st.session_state["dataset_id"] = file_name
                st.session_state["ocr_df"] = edited_df

                st.success("✅ Dataset OCR guardado")

                st.rerun()

    # ==================================================
    # TAB 2
    # ==================================================
    with tabs[1]:

        source_type = st.selectbox(
            "Tipo de fuente",
            ["postgres", "mysql", "api", "google_sheets"]
        )

        config = {}

        if source_type in ["postgres", "mysql"]:
            config["uri"] = st.text_input("Connection string")

        elif source_type == "api":
            config["base_url"] = st.text_input("Base URL")

        elif source_type == "google_sheets":
            config["url"] = st.text_input("Google Sheet URL")

        if st.button("Conectar"):

            connector = create_connector(
                source_type,
                config
            )

            st.session_state["connector"] = connector

            dataset_id = get_dataset_id(
                source_type,
                config
            )

            st.session_state["dataset_id"] = dataset_id

            loaded = load_semantic_layer(dataset_id)

            if loaded:
                st.session_state["semantic_layer"] = loaded

            st.success