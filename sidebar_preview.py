import streamlit as st

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("📊 App Data IA Analisis")

     # 🔥 DATASET ACTIVO (SIEMPRE VISIBLE)
    if "file_path" in st.session_state:
        import os
        st.success(f"📊 Dataset:\n{os.path.basename(st.session_state['file_path'])}")
    else:
        st.warning("No hay dataset activo")
        
    st.button("🆕 Nueva conversación", key="chat_new")

    st.markdown("---")

    with st.expander("📥 Ingresar Datos"):
        st.button("+ Crear", key="data_create")
        st.button("Fuente externa (1ra vez)", key="data_external")

    with st.expander("🧠 Fuentes / Semántica"):
        st.button("Editar fuentes", key="semantic_sources")
        st.button("Editar métricas", key="semantic_metrics")
        st.button("Aliases", key="semantic_alias")

    with st.expander("📚 Datasets"):
        st.button("Ver / Gestionar", key="datasets_manage")

    with st.expander("📊 Gráficos"):
        st.button("Línea", key="chart_line")
        st.button("Barras", key="chart_bar")
        st.button("Torta", key="chart_pie")
        st.button("Doble línea", key="chart_double_line")
        st.button("Cascada", key="chart_waterfall")
        st.button("Forecast", key="chart_forecast")  # 👈 clave

    with st.expander("🤖 Machine Learning"):
        st.button("Churn", key="ml_churn")
        st.button("Forecast", key="ml_forecast")  # 👈 diferente
        st.button("Canasta / Promos", key="ml_basket")
        st.button("Scoring", key="ml_scoring")
        st.button("Alertas (Stock / Ventas)", key="ml_alerts")

    with st.expander("🏆 Queries Ranking"):
        st.button("Top", key="ranking_top")
        st.button("Bottom", key="ranking_bottom")
        st.button("Comparaciones", key="ranking_compare")

    st.markdown("---")

    with st.expander("🕓 Recientes", expanded=True):
        for i in range(7):
            st.button(f"Conversación {i+1}", key=f"recent_{i}")