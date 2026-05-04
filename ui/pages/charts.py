import streamlit as st

def render_charts():

    st.title("📊 Visualización")

    tabs = st.tabs([
        "📈 Línea",
        "📊 Barras",
        "🥧 Torta",
        "📉 Forecast"
    ])

    # -------------------------
    # 📈 LINE
    # -------------------------
    with tabs[0]:
        st.selectbox("Eje X", ["fecha"])
        st.selectbox("Eje Y", ["ventas"])
        st.button("Generar gráfico")

    # -------------------------
    # 📊 BAR
    # -------------------------
    with tabs[1]:
        st.selectbox("Categoría", ["producto"])
        st.selectbox("Valor", ["ventas"])
        st.button("Generar gráfico")

    # -------------------------
    # 🥧 PIE
    # -------------------------
    with tabs[2]:
        st.selectbox("Segmento", ["cliente"])
        st.selectbox("Valor", ["ventas"])
        st.button("Generar gráfico")

    # -------------------------
    # 📉 FORECAST
    # -------------------------
    with tabs[3]:
        st.selectbox("Serie", ["ventas"])
        st.button("Generar forecast")