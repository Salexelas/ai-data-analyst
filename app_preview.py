import streamlit as st

st.set_page_config(layout="wide")

# =========================
# 🔹 STATE GLOBAL (router)
# =========================
if "page" not in st.session_state:
    st.session_state.page = "chat"

# =========================
# 🔹 SIDEBAR
# =========================
with st.sidebar:
    st.title("📊 App Data IA Analisis")

    if st.button("🆕 Nueva conversación", key="chat_new"):
        st.session_state.page = "chat"

    st.markdown("---")

    with st.expander("📥 Ingresar Datos"):
        if st.button("+ Crear", key="data_create"):
            st.session_state.page = "data_create"

        if st.button("Fuente externa (1ra vez)", key="data_external"):
            st.session_state.page = "data_external"

    with st.expander("🧠 Fuentes / Semántica"):
        if st.button("Editar fuentes", key="semantic_sources"):
            st.session_state.page = "semantic"

        if st.button("Editar métricas", key="semantic_metrics"):
            st.session_state.page = "semantic"

        if st.button("Aliases", key="semantic_alias"):
            st.session_state.page = "semantic"

    with st.expander("📊 Gráficos"):
        if st.button("Línea", key="chart_line"):
            st.session_state.page = "charts"

        if st.button("Barras", key="chart_bar"):
            st.session_state.page = "charts"

        if st.button("Torta", key="chart_pie"):
            st.session_state.page = "charts"

        if st.button("Doble línea", key="chart_double_line"):
            st.session_state.page = "charts"

        if st.button("Cascada", key="chart_waterfall"):
            st.session_state.page = "charts"

        if st.button("Forecast", key="chart_forecast"):
            st.session_state.page = "charts"

    with st.expander("🤖 Machine Learning"):
        if st.button("Churn", key="ml_churn"):
            st.session_state.page = "ml"

        if st.button("Forecast", key="ml_forecast"):
            st.session_state.page = "ml"

        if st.button("Canasta / Promos", key="ml_basket"):
            st.session_state.page = "ml"

        if st.button("Scoring", key="ml_scoring"):
            st.session_state.page = "ml"

        if st.button("Alertas (Stock / Ventas)", key="ml_alerts"):
            st.session_state.page = "ml"

    with st.expander("🏆 Queries Ranking"):
        if st.button("Top", key="ranking_top"):
            st.session_state.page = "ranking"

        if st.button("Bottom", key="ranking_bottom"):
            st.session_state.page = "ranking"

        if st.button("Comparaciones", key="ranking_compare"):
            st.session_state.page = "ranking"

    st.markdown("---")

    with st.expander("🕓 Recientes", expanded=True):
        for i in range(7):
            st.button(f"Conversación {i+1}", key=f"recent_{i}")

# =========================
# 🔥 MAIN ROUTER
# =========================

# =========================
# 💬 CHAT
# =========================
if st.session_state.page == "chat":

    st.title("💬 Nueva conversación")

    tabs = st.tabs(["💬 Chat", "🔀 Comparación", "📈 Vista"])

    # TAB CHAT
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

    # TAB COMPARACIÓN
    with tabs[1]:
        st.markdown("### 🔀 Comparar datasets")

        col1, col2 = st.columns(2)

        with col1:
            st.selectbox("Tabla A", ["ventas", "clientes"], key="table_a")

        with col2:
            st.selectbox("Tabla B", ["ventas", "clientes"], key="table_b")

        st.button("Comparar", key="compare_run")

    # TAB VISTA
    with tabs[2]:
        st.markdown("### 📈 Opciones de vista")
        st.checkbox("Modo compacto")
        st.checkbox("Mostrar insight")
        st.checkbox("Mostrar SQL")

# =========================
# 📥 DATA CREATE
# =========================
elif st.session_state.page == "data_create":

    st.title("📥 Crear dataset")

    tabs = st.tabs(["📂 Subir archivo", "🔗 Conectar", "⚙️ Config"])

    with tabs[0]:
        st.file_uploader("Subir CSV / Excel")
        st.button("Cargar")

    with tabs[1]:
        st.text_input("URL / DB string")
        st.button("Conectar")

    with tabs[2]:
        st.checkbox("Detectar tipos automáticamente")
        st.checkbox("Normalizar columnas")

# =========================
# 🌐 DATA EXTERNAL
# =========================
elif st.session_state.page == "data_external":

    st.title("🌐 Fuente externa")

    tabs = st.tabs(["🔗 API", "🗄️ Base de datos", "📊 Preview"])

    with tabs[0]:
        st.text_input("Endpoint API")
        st.button("Test API")

    with tabs[1]:
        st.text_input("Connection string")
        st.button("Conectar DB")

    with tabs[2]:
        st.info("Preview de datos")

# =========================
# 🧠 SEMANTIC
# =========================
elif st.session_state.page == "semantic":

    st.title("🧠 Semántica")

    tabs = st.tabs(["🔤 Aliases", "📊 Métricas", "🧪 Test"])

    with tabs[0]:
        st.text_input("Columna → alias")

    with tabs[1]:
        st.text_input("Nueva métrica")
        st.text_input("SQL")

    with tabs[2]:
        st.text_input("Test query")
        st.button("Probar")

# =========================
# 📊 CHARTS
# =========================
elif st.session_state.page == "charts":

    st.title("📊 Gráficos")

    tabs = st.tabs(["📈 Línea", "📊 Barras", "🥧 Torta", "📉 Forecast"])

    with tabs[0]:
        st.selectbox("Eje X", ["fecha"])
        st.selectbox("Eje Y", ["ventas"])
        st.button("Generar línea")

    with tabs[1]:
        st.selectbox("Categoría", ["producto"])
        st.selectbox("Valor", ["ventas"])
        st.button("Generar barras")

    with tabs[2]:
        st.selectbox("Segmento", ["cliente"])
        st.selectbox("Valor", ["ventas"])
        st.button("Generar torta")

    with tabs[3]:
        st.selectbox("Serie", ["ventas"])
        st.button("Generar forecast")

# =========================
# 🤖 ML
# =========================
elif st.session_state.page == "ml":

    st.title("🤖 Machine Learning")

    tabs = st.tabs(["📉 Churn", "📈 Forecast", "🛒 Canasta", "🎯 Scoring"])

    with tabs[0]:
        st.selectbox("Target", ["churn"])
        st.button("Entrenar modelo")

    with tabs[1]:
        st.selectbox("Serie temporal", ["ventas"])
        st.button("Predecir")

    with tabs[2]:
        st.button("Analizar productos frecuentes")

    with tabs[3]:
        st.button("Generar scoring")

# =========================
# 🏆 RANKING
# =========================
elif st.session_state.page == "ranking":

    st.title("🏆 Ranking / Queries")

    tabs = st.tabs(["🔝 Top", "🔻 Bottom", "⚖️ Comparaciones"])

    with tabs[0]:
        st.selectbox("Métrica", ["ventas"])
        st.button("Top 10")

    with tabs[1]:
        st.selectbox("Métrica", ["ventas"])
        st.button("Bottom 10")

    with tabs[2]:
        st.text_input("Comparar entidades")
        st.button("Comparar")