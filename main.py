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
    ["duckdb", "postgres", "mysql", "excel", "csv","google_sheets" ,"api"]
)

config = {}

# -------------------------
# INPUTS DINÁMICOS
# -------------------------

if source_type == "duckdb":
    use_demo = st.checkbox("Usar tabla demo (sin subir archivo)", value=True)

    uploaded_file = None
    if not use_demo:
        uploaded_file = st.file_uploader(
            "Subí CSV/Parquet",
            type=["csv", "parquet"]
        )

    # Guardar en config
    if uploaded_file:
        config["file"] = uploaded_file
    elif use_demo:
        config["file"] = None  # DuckDBConnector detecta None y carga demo

elif source_type in ["postgres", "mysql"]:
    use_demo = st.checkbox("Usar tabla demo (sin conexión real)", value=True)

    if use_demo:
        config["uri"] = None  # el conector detecta None y carga demo
    else:
        default_uri = (
            "postgresql://user:pass@localhost:5432/db"
            if source_type == "postgres"
            else "mysql+pymysql://user:pass@localhost:3306/db"
        )
        config["uri"] = st.text_input("🔗 Pegá tu Connection String", default_uri)

elif source_type == "google_sheets":
    config["url"] = st.text_input("Pegá tu Google Sheet")

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

        st.subheader("📊 Tipos de datos")
        st.write(preview.dtypes)

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