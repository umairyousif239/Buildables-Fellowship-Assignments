# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Sanity check
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")
if not ANTHROPIC_API_KEY:
    raise ValueError("Missing ANTHROPIC_API_KEY in .env")