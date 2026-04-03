import streamlit as st
from connectors.factory import create_connector

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🔥 AI Data Analyst")
st.write("Conectá tu fuente de datos en segundos")

# -------------------------
# SELECTOR DE SOURCE
# -------------------------

source_type = st.selectbox(
    "Seleccioná tipo de fuente",
    ["duckdb", "postgres", "mysql", "excel", "csv", "api"]
)

config = {}

# -------------------------
# INPUTS DINÁMICOS
# -------------------------

if source_type == "duckdb":
    config["path"] = st.text_input("Ruta DB", "data/sample.duckdb")

elif source_type == "postgres":
    config["uri"] = st.text_input("URI", "postgresql://user:pass@localhost/db")

elif source_type == "mysql":
    config["uri"] = st.text_input("URI", "mysql://user:pass@localhost/db")

elif source_type == "api":
    config["base_url"] = st.text_input("Base URL", "https://api.example.com")

# 🔥 ACÁ ESTÁ LO IMPORTANTE (drag & drop)
elif source_type in ["excel", "csv"]:

    uploaded_file = st.file_uploader(
        "📂 Arrastrá tu archivo (CSV o Excel)",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        config["file"] = uploaded_file


# -------------------------
# CONNECT BUTTON
# -------------------------

if st.button("🚀 Conectar"):

    try:
        # Validación para archivos
        if source_type in ["excel", "csv"] and "file" not in config:
            st.warning("⚠️ Subí un archivo primero")
            st.stop()

        connector = create_connector(source_type, config)

        st.success("✅ Conexión exitosa")

        # -------------------------
        # SCHEMA
        # -------------------------
        st.subheader("📚 Schema")
        schema = connector.get_schema()
        st.dataframe(schema)

        # -------------------------
        # PREVIEW
        # -------------------------
        st.subheader("👀 Preview")
        preview = connector.preview()
        st.dataframe(preview)

        # Columnas detectadas (pro level)
        st.subheader("🧠 Columnas detectadas")
        st.write(list(preview.columns))

        # Guardar en session
        st.session_state["connector"] = connector

    except Exception as e:
        st.error(f"❌ Error de conexión: {str(e)}")


# -------------------------
# QUERY SECTION
# -------------------------

if "connector" in st.session_state:

    st.subheader("💬 Hacer pregunta")

    question = st.text_input("Pregunta")

    if st.button("Ejecutar"):

        try:
            from agents.router import route_question

            result = route_question(
                question,
                st.session_state["connector"]
            )

            st.subheader("📊 Resultado")
            st.dataframe(result)

        except Exception as e:
            st.error(f"❌ Error en la query: {str(e)}")