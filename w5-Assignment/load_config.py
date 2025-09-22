import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

if not HUGGINGFACE_API_KEY:
    raise ValueError("Missing HUGGINGFACE_API_KEY in .env")

print("configuration successful...")