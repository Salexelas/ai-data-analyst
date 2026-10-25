import streamlit as st
from streamlit_mic_recorder import mic_recorder


def render_audio_input():

    audio = mic_recorder(
        start_prompt="🎤 Hablar",
        stop_prompt="⏹️ Detener",
       # just_once=True,
        key="mic_recorder"
    )

    return audio