'''import streamlit as st
import pandas as pd
import os
import json

from connectors.factory import create_connector

# ==================================================
# PATHS
# ==================================================
DATA_PATH = "data"
SCHEMA_PATH = "schemas"

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(SCHEMA_PATH, exist_ok=True)

# ==================================================
# COLUMN TYPES
# ==================================================
TYPE_OPTIONS = [
    "auto",
    "text",
    "number",
    "datetime",
    "boolean",
    "category",
    "id"
]

# ==================================================
# LOAD SCHEMA
# ==================================================
def load_schema(dataset_name):

    schema_file = os.path.join(
        SCHEMA_PATH,
        f"{dataset_name}.schema.json"
    )

    if not os.path.exists(schema_file):
        return {}

    try:

        with open(schema_file, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return {}

# ==================================================
# SAVE SCHEMA
# ==================================================
def save_schema(dataset_name, schema):

    schema_file = os.path.join(
        SCHEMA_PATH,
        f"{dataset_name}.schema.json"
    )

    with open(schema_file, "w", encoding="utf-8") as f:

        json.dump(
            schema,
            f,
            indent=4,
            ensure_ascii=False
        )

# ==================================================
# DETECT DEFAULT TYPE
# ==================================================
def detect_default_type(series):

    dtype = str(series.dtype)

    if "datetime" in dtype:
        return "datetime"

    if "int" in dtype or "float" in dtype:
        return "number"

    if "bool" in dtype:
        return "boolean"

    return "text"

# ==================================================
# APPLY COLUMN TYPES
# ==================================================
def apply_column_types(df, schema):

    for col, dtype in schema.items():

        if col not in df.columns:
            continue

        try:

            # -------------------------
            # DATETIME
            # -------------------------
            if dtype == "datetime":

                df[col] = pd.to_datetime(
                    df[col],
                    dayfirst=True,
                    errors="coerce"
                )

            # -------------------------
            # NUMBER
            # -------------------------
            elif dtype == "number":

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

            # -------------------------
            # BOOLEAN
            # -------------------------
            elif dtype == "boolean":

                df[col] = df[col].astype("bool")

            # -------------------------
            # CATEGORY
            # -------------------------
            elif dtype == "category":

                df[col] = df[col].astype("category")

            # -------------------------
            # TEXT
            # -------------------------
            elif dtype == "text":

                df[col] = df[col].astype("string")

        except Exception as e:

            st.warning(f"Error casteando {col}: {e}")

    return df

# ==================================================
# MAIN
# ==================================================
def render_dataset_editor():

    st.title("✏️ Editor de Dataset")

    # ==================================================
    # SESSION
    # ==================================================
    file_path = st.session_state.get("file_path")

    if not file_path:

        st.warning("Primero cargá un dataset")
        return

    if not os.path.exists(file_path):

        st.error("El archivo no existe")
        return

    file_name = os.path.basename(file_path)

    # ==================================================
    # FILE TYPE
    # ==================================================
    if file_name.endswith(".csv"):

        file_type = "csv"

    elif file_name.endswith(".xlsx"):

        file_type = "excel"

    else:

        st.error("Formato no soportado")
        return

    # ==================================================
    # LOAD DATAFRAME
    # ==================================================
    try:

        connector = create_connector(
            file_type,
            {"file_path": file_path}
        )

        df = connector.preview(100000)

    except Exception as e:

        st.error(f"Error cargando dataset: {e}")
        return

    # ==================================================
    # LOAD EXISTING SCHEMA
    # ==================================================
    schema = load_schema(file_name)

    # ==================================================
    # TABS
    # ==================================================
    tabs = st.tabs([
        "📝 Columnas",
        "🧠 Tipos",
        "📊 Datos"
    ])

    # ==================================================
    # 📝 COLUMNAS
    # ==================================================
    with tabs[0]:

        st.subheader("📝 Renombrar columnas")

        rename_map = {}

        cols = st.columns(2)

        for i, col in enumerate(df.columns):

            with cols[i % 2]:

                new_name = st.text_input(
                    f"{col}",
                    value=col,
                    key=f"rename_{col}"
                )

                rename_map[col] = new_name

    # ==================================================
    # 🧠 TIPOS
    # ==================================================
    with tabs[1]:

        st.subheader("🧠 Tipos de columnas")

        column_types = {}

        cols = st.columns(2)

        for i, col in enumerate(df.columns):

            with cols[i % 2]:

                saved_type = schema.get(col)

                default_type = (
                    saved_type
                    if saved_type
                    else detect_default_type(df[col])
                )

                column_types[col] = st.selectbox(
                    f"Tipo → {col}",
                    TYPE_OPTIONS,
                    index=TYPE_OPTIONS.index(default_type),
                    key=f"type_{col}"
                )

    # ==================================================
    # APPLY TYPES
    # ==================================================
    df = apply_column_types(
        df,
        column_types
    )

    # ==================================================
    # 📊 DATOS
    # ==================================================
    with tabs[2]:

        st.subheader("📊 Editor")

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            height=600
        )

    # ==================================================
    # APPLY RENAME
    # ==================================================
    edited_df.columns = [
        rename_map[c]
        for c in edited_df.columns
    ]

    # ==================================================
    # SAVE
    # ==================================================
    st.divider()

    if st.button("💾 Guardar cambios"):

        try:

            # ==================================================
            # SAVE DATASET
            # ==================================================
            if file_type == "csv":

                edited_df.to_csv(
                    file_path,
                    index=False
                )

            else:

                edited_df.to_excel(
                    file_path,
                    index=False
                )

            # ==================================================
            # UPDATE SCHEMA
            # ==================================================
            updated_schema = {}

            for old_col, new_col in rename_map.items():

                updated_schema[new_col] = column_types[old_col]

            save_schema(
                file_name,
                updated_schema
            )

            # ==================================================
            # RELOAD CONNECTOR
            # ==================================================
            connector = create_connector(
                file_type,
                {"file_path": file_path}
            )

            st.session_state["connector"] = connector

            # invalidate semantic layer
            st.session_state["semantic_layer"] = None

            st.success("✅ Dataset actualizado")

            st.rerun()

        except Exception as e:

            st.error(f"Error guardando dataset: {e}")


'''