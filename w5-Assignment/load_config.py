import os
import streamlit as st
from dotenv import load_dotenv

# Load .env only when running locally
load_dotenv()

class Config:
    # Try secrets first, then fallback to .env
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")

    # Debug messages
    if GEMINI_API_KEY:
        if "GEMINI_API_KEY" in st.secrets:
            print("✅ Loaded GEMINI_API_KEY from Streamlit secrets")
        else:
            print("✅ Loaded GEMINI_API_KEY from .env")

    if HUGGINGFACE_API_KEY:
        if "HUGGINGFACE_API_KEY" in st.secrets:
            print("✅ Loaded HUGGINGFACE_API_KEY from Streamlit secrets")
        else:
            print("✅ Loaded HUGGINGFACE_API_KEY from .env")

    # Raise errors if missing
    if not GEMINI_API_KEY:
        raise ValueError("❌ Missing GEMINI_API_KEY in secrets or .env")

    if not HUGGINGFACE_API_KEY:
        raise ValueError("❌ Missing HUGGINGFACE_API_KEY in secrets or .env")
