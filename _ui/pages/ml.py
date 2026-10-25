import streamlit as st

def render_ml():

    st.title("🤖 Machine Learning")

    tabs = st.tabs(["📉 Churn", "📈 Forecast"])

    with tabs[0]:
        st.button("Entrenar churn")

    with tabs[1]:
        st.button("Predecir")