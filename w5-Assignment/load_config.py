import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = st.secrets["default"].get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    HUGGINGFACE_API_KEY = st.secrets["default"].get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")

    if not GEMINI_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY in secrets or .env")

    if not HUGGINGFACE_API_KEY:
        raise ValueError("Missing HUGGINGFACE_API_KEY in secrets or .env")

    print("configuration successful...")
