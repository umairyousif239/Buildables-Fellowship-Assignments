# src/utils/llm_setup.py

import os
import sys
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from load_config import GEMINI_API_KEY


# -----------------------------
# Initialize Hugging Face Embeddings
# -----------------------------
embeddings = None
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("[INFO] Hugging Face embeddings initialized successfully.")
except Exception as e:
    print(f"[ERROR] Failed to initialize embeddings: {e}")
    raise RuntimeError(f"Embeddings initialization failed: {e}")


# -----------------------------
# Initialize Gemini LLM (Hosted API, no local storage)
# -----------------------------
llm = None
try:
    genai.configure(api_key=GEMINI_API_KEY)
    _gemini_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "max_output_tokens": 120,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    def llm(prompt: str):
        """Simple callable that returns plain text from Gemini."""
        resp = _gemini_model.generate_content(prompt)
        return getattr(resp, "text", str(resp))

    print("[INFO] Gemini LLM (gemini-1.5-flash) initialized successfully.")
except Exception as e:
    print(f"[ERROR] Failed to initialize Gemini LLM: {e}")