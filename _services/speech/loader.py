import streamlit as st
from services.speech.whisper_service import WhisperService


@st.cache_resource
def load_whisper():
    return WhisperService()