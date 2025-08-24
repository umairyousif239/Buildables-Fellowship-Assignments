import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import logging
from typing import Dict, Any
from dotenv import load_dotenv

import google.generativeai as genai
from openai import OpenAI           # DeepSeek uses OpenAI-compatible API
from project_config import GEMINI_API_KEY, DEEPSEEK_API_KEY

# API CLIENTS

# Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# DeepSeek
deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# MODEL COSTS (example values, replace with actual pricing from docs)
MODEL_COSTS = {
    "gemini": {"input": 0.0005, "output": 0.0015}, # per 1k tokens
    "deepseek": {"input": 0.0003, "output": 0.0009},
}

# Helper: Safe API Call
def safe_api_call(api_func, *args, retries=3, wait=2, **kwargs) -> Any:
    """Wrapper to safely call API functions with retries and logging."""
    for attempt in range(retries):
        try:
            return api_func(*args, **kwargs)
        except Exception as e:
            logging.warning(f"API call failed (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(wait * (attempt + 1))
            else:
                raise RuntimeError("API call failed after retries") from e

# LLM CALLS
def summarize_with_gemini(text: str) -> str:
    """Summarize text using Gemini API."""
    def _call():
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Summarize this text clearly:\n\n{text}")
        return response.text

    return safe_api_call(_call)


def summarize_with_deepseek(text: str) -> str:
    """Summarize text using DeepSeek API."""
    def _call():
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize this text clearly:\n\n{text}"}
            ]
        )
        return response.choices[0].message.content

    return safe_api_call(_call)

# Unified API
def summarize(text: str, model: str) -> str:
    """Route summarization request to the right model."""
    if model == "gemini":
        return summarize_with_gemini(text)
    elif model == "deepseek":
        return summarize_with_deepseek(text)
    else:
        raise ValueError(f"Unsupported model: {model}")

# Cost Estimation
def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Estimate API cost based on token usage."""
    costs = MODEL_COSTS.get(model, {})
    if not costs:
        return 0.0

    total = (input_tokens / 1000) * costs["input"] + (output_tokens / 1000) * costs["output"]
    return round(total, 6)