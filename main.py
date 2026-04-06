import streamlit as st
import json
import os
import hashlib

from connectors.factory import create_connector
from semantic.semantic_layer import build_semantic_layer, merge_semantic_layers
from semantic.semantic_agent import generate_semantic_suggestions

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🔥 AI Data Analyst")
st.write("Conectá tu fuente de datos en segundos")

# -------------------------
# HELPERS
# -------------------------

def get_dataset_id(source_type, config):
    base = f"{source_type}_{str(config)}"
    return hashlib.md5(base.encode()).hexdigest()


def save_semantic_layer(dataset_id, semantic_layer):
    os.makedirs("semantic_store", exist_ok=True)
    path = f"semantic_store/{dataset_id}.json"

    with open(path, "w") as f:
        json.dump(semantic_layer, f, indent=2)


def load_semantic_layer(dataset_id):
    path = f"semantic_store/{dataset_id}.json"

    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)

    return None


def list_semantic_files():
    path = "semantic_store"
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if f.endswith(".json")]


def load_semantic_file(file_name):
    path = os.path.join("semantic_store", file_name)
    with open(path) as f:
        return json.load(f)


# -------------------------
# SELECTOR DE SOURCE
# -------------------------

source_type = st.selectbox(
    "Seleccioná tipo de fuente",
    ["duckdb", "postgres", "mysql", "excel", "csv", "google_sheets", "api"]
)

config = {}

# -------------------------
# INPUTS DINÁMICOS
# -------------------------

if source_type == "duckdb":
    use_demo = st.checkbox("Usar tabla demo", value=True)

    uploaded_file = None
    if not use_demo:
        uploaded_file = st.file_uploader("Subí CSV/Parquet", type=["csv", "parquet"])

    if uploaded_file:
        config["file"] = uploaded_file
    elif use_demo:
        config["file"] = None

elif source_type in ["postgres", "mysql"]:
    use_demo = st.checkbox("Usar demo", value=True)

    if use_demo:
        config["uri"] = None
    else:
        default_uri = (
            "postgresql://user:pass@localhost:5432/db"
            if source_type == "postgres"
            else "mysql+pymysql://user:pass@localhost:3306/db"
        )
        config["uri"] = st.text_input("Connection String", default_uri)

elif source_type == "google_sheets":
    config["url"] = st.text_input("Google Sheet URL")

elif source_type == "api":
    config["base_url"] = st.text_input("Base URL", "https://api.example.com")

elif source_type in ["excel", "csv"]:
    uploaded_file = st.file_uploader("📂 Subí archivo", type=["csv", "xlsx"])

    if uploaded_file:
        config["file"] = uploaded_file


# -------------------------
# CONNECT
# -------------------------

if st.button("🚀 Conectar"):
    try:
        if source_type in ["excel", "csv"] and "file" not in config:
            st.warning("⚠️ Subí un archivo primero")
            st.stop()

        connector = create_connector(source_type, config)
        st.session_state["connector"] = connector

        dataset_id = get_dataset_id(source_type, config)
        st.session_state["dataset_id"] = dataset_id

        loaded = load_semantic_layer(dataset_id)
        if loaded:
            st.session_state["semantic_layer"] = loaded
            st.info("📂 Capa semántica cargada")

        st.success("✅ Conectado")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


# -------------------------
# DATA VIEW
# -------------------------

if "connector" in st.session_state:

    connector = st.session_state["connector"]

    st.subheader("📚 Schema")
    st.dataframe(connector.get_schema())

    st.subheader("👀 Preview")
    preview = connector.preview()
    st.dataframe(preview)

    columns = list(preview.columns)

    st.subheader("🧠 Columnas")
    st.write(columns)

    st.subheader("📊 Tipos")
    st.write(preview.dtypes)

    # -------------------------
    # 🔥 NUEVO: MULTI SEMANTIC
    # -------------------------

    st.subheader("🧠 Usar Semantic Layers existentes")

    semantic_files = list_semantic_files()

    if semantic_files:

        col1, col2 = st.columns(2)

        with col1:
            sem1_name = st.selectbox("Semantic 1", ["None"] + semantic_files)

        with col2:
            sem2_name = st.selectbox("Semantic 2", ["None"] + semantic_files)

        if st.button("📥 Aplicar Semantic Layers"):

            sem1 = load_semantic_file(sem1_name) if sem1_name != "None" else None
            sem2 = load_semantic_file(sem2_name) if sem2_name != "None" else None

            merged = merge_semantic_layers(sem1, sem2)

            st.session_state["semantic_layer"] = merged

            st.success("✅ Semantic layers aplicadas")

            st.json(merged)

    # -------------------------
    # GENERAR NUEVA
    # -------------------------

    st.subheader("✨ Generar nueva semántica")

    if st.button("Generar automáticamente"):
        raw = generate_semantic_suggestions(columns)

        st.session_state["semantic_layer"] = build_semantic_layer(
            columns,
            raw.get("aliases"),
            raw.get("metrics")
        )

        st.success("✅ Generada")

    # -------------------------
    # EDITAR
    # -------------------------

    if "semantic_layer" in st.session_state:

        sl = st.session_state["semantic_layer"]

        st.write("### 🔤 Aliases")
        st.json(sl["aliases"])

        st.write("### 📊 Métricas")
        st.json(sl["metrics"])

        # EDITAR
        st.write("### ✏️ Editar Aliases")

        for col in columns:
            current = sl["aliases"].get(col, [])
            key_name = f"alias_{col}"

            if key_name not in st.session_state:
                st.session_state[key_name] = ", ".join(current)

            value = st.text_input(col, key=key_name)

            sl["aliases"][col] = [v.strip() for v in value.split(",") if v]

        st.write("### ✏️ Editar Métricas")

        for k, v in list(sl["metrics"].items()):
            key_name = f"metric_{k}"

            if key_name not in st.session_state:
                st.session_state[key_name] = v

            new_val = st.text_input(k, key=key_name)
            sl["metrics"][k] = new_val

        # AGREGAR
        st.write("### ➕ Nueva Métrica")

        new_name = st.text_input("Nombre")
        new_expr = st.text_input("SQL")

        if st.button("Agregar métrica"):
            if new_name and new_expr:
                sl["metrics"][new_name] = new_expr
                st.success(f"✅ {new_name} agregada")

        # GUARDAR
        if st.button("💾 Guardar capa semántica"):
            save_semantic_layer(
                st.session_state["dataset_id"],
                sl
            )
            st.success("✅ Guardado")

        st.session_state["semantic_layer"] = sl

# -------------------------
# QUERY
# -------------------------

if "connector" in st.session_state:

    st.subheader("💬 Pregunta")

    question = st.text_input("Escribí tu pregunta")

    if st.button("Ejecutar"):

        try:
            from agents.router import route_question

            result = route_question(
                question,
                st.session_state["connector"],
                st.session_state.get("semantic_layer"),
                st.session_state.get("dataset_id")
            )

            st.subheader("📊 Resultado")
            st.dataframe(result)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")