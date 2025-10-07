import streamlit as st
from pathlib import Path


def load_css(file_name: str):
    file_path = Path(f"src/static/css/{file_name}").resolve()
    with Path.open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")
