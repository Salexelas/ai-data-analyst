import streamlit as st

st.set_page_config(layout="wide")

# 🔹 SIDEBAR (lo dejamos intacto)
with st.sidebar:
    st.title("📊 App Data IA Analisis")

    st.button("🆕 Nueva conversación", key="chat_new")

    st.markdown("---")

    with st.expander("📥 Ingresar Datos"):
        st.button("+ Crear", key="data_create")
        st.button("Fuente externa", key="data_external")

    with st.expander("🧠 Fuentes / Semántica"):
        st.button("Editar fuentes", key="semantic_sources")

    with st.expander("📊 Gráficos"):
        st.button("Línea", key="chart_line")

    with st.expander("🤖 Machine Learning"):
        st.button("Churn", key="ml_churn")

    with st.expander("🏆 Queries Ranking"):
        st.button("Top", key="ranking_top")

# 🔥 MAIN — con solapas (tabs)

st.title("💬 Nueva conversación")

tabs = st.tabs([
    "💬 Chat",
    "🔀 Comparación",
    "📈 Vista"
])

# =========================
# 💬 TAB 1 — CHAT
# =========================
with tabs[0]:
    st.text_input("Escribí tu pregunta...")

    col1, col2 = st.columns([1,1])

    with col1:
        st.button("Ejecutar", key="chat_run")

    with col2:
        st.button("Limpiar", key="chat_clear")

    st.markdown("---")

    st.subheader("📊 Resultado")
    st.info("Acá se muestra la tabla")

    st.subheader("🧠 Insight")
    st.info("Acá se muestra el análisis")

# =========================
# 🔀 TAB 2 — COMPARACIÓN
# =========================
with tabs[1]:
    st.markdown("### 🔀 Comparar datasets")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox("Tabla A", ["ventas", "clientes"], key="table_a")

    with col2:
        st.selectbox("Tabla B", ["ventas", "clientes"], key="table_b")

    st.button("Comparar", key="compare_run")

    st.markdown("---")

    st.subheader("📊 Resultado comparación")
    st.info("Resultado comparativo")

# =========================
# 📈 TAB 3 — VISTA
# =========================
with tabs[2]:
    st.markdown("### 📈 Opciones de vista")

    st.checkbox("Modo compacto")
    st.checkbox("Mostrar insight")
    st.checkbox("Mostrar SQL")