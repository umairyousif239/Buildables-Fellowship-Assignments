# src/agent.py

from src.utils.llm_setup import llm
from src.utils.db import search
from src.tools.sentiment import analyze_sentiment

PREFERRED_KEYS = ("generated_text", "text", "content", "response", "message")

# -----------------------------
# Return the value if it is a non-empty string; otherwise None.
# -----------------------------
def _coerce_str(value):
    return value if isinstance(value, str) and value.strip() else None

# -----------------------------
# Pull the first meaningful string from a dict, preferring known keys.
# -----------------------------
def _extract_from_dict(d):
    for k in PREFERRED_KEYS:
        v = _coerce_str(d.get(k))
        if v is not None:
            return v
    for v in d.values():
        sv = _coerce_str(v)
        if sv is not None:
            return sv
    return None

# -----------------------------
# Normalize various LLM response shapes into a plain string.
# -----------------------------
def extract_text(resp):
    """
    Normalize various LLM response formats into a plain string.
    """
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        v = _extract_from_dict(resp)
        return v if v is not None else str(resp)
    if isinstance(resp, (list, tuple)):
        return extract_text(resp[0]) if len(resp) > 0 else str(resp)
    return str(resp)

# -----------------------------
# Join retrieved past entry texts into a context block.
# -----------------------------
def build_context(past_entries):
    """
    Build a newline-joined context from past entries search results.
    """
    try:
        return "\n".join([doc[0].page_content for doc in past_entries])  # doc[0] is Document
    except Exception:
        return ""

# -----------------------------
# Build a concise journaling prompt with input, sentiment, and context.
# -----------------------------
def build_prompt(user_input: str, sentiment: str, context: str) -> str:
    """
    Construct the journaling assistant prompt.
    """
    return f"""
    You are a reflective journaling assistant.
    User just wrote: "{user_input}".
    Sentiment detected: {sentiment}.
    Here are related past entries:
    {context}

    Based on this, give an empathetic reflection.
    Suggest patterns, insights, or advice if relevant.
    Keep it brief and journal-friendly: 3–4 sentences, under 90 words.
    """

# -----------------------------
# Generate a brief reflection: analyze sentiment, retrieve context, prompt LLM.
# -----------------------------
def reflect(db, user_input: str) -> str:
    """
    Reflective journaling assistant.
    Steps:
    1. Analyze sentiment of new entry.
    2. Retrieve similar past entries from FAISS DB.
    3. Build prompt including context and sentiment.
    4. Generate a concise reflection using the configured LLM.
    """
    # Step 1: Sentiment of new entry
    sentiment = analyze_sentiment(user_input)

    # Step 2: Retrieve similar past entries
    past_entries = search(db, user_input, k=3)
    context = build_context(past_entries)

    # Step 3: Build prompt
    prompt = build_prompt(user_input, sentiment, context)

    # Step 4: Get response from Hugging Face LLM
    try:
        raw_response = llm(prompt)
        print(f"[DEBUG] Raw LLM response: {raw_response}")  # For debugging
        return extract_text(raw_response)
    except Exception as e:
        # Catch errors like API key issues
        return f"[ERROR] LLM failed: {str(e)}"
