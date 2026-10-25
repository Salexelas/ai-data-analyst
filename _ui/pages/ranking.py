import streamlit as st

def render_ranking():

    st.title("🏆 Ranking & Queries")

    tabs = st.tabs([
        "🔝 Top",
        "🔻 Bottom",
        "⚖️ Comparación"
    ])

    # -------------------------
    # TOP
    # -------------------------
    with tabs[0]:
        st.selectbox("Métrica", ["ventas", "clientes"])
        st.number_input("Cantidad", 1, 100, 10)
        st.button("Ejecutar Top")

    # -------------------------
    # BOTTOM
    # -------------------------
    with tabs[1]:
        st.selectbox("Métrica", ["ventas", "clientes"])
        st.number_input("Cantidad", 1, 100, 10, key="bottom_n")
        st.button("Ejecutar Bottom")

    # -------------------------
    # COMPARISON
    # -------------------------
    with tabs[2]:
        st.text_input("Entidad A")
        st.text_input("Entidad B")
        st.button("Comparar")

        st.markdown("---")
        st.subheader("Resultado")
        st.info("Resultado comparativo")