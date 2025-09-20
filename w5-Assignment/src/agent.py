# src/agent.py

from src.utils.llm_setup import llm
from src.utils.db import search
from src.tools.sentiment import analyze_sentiment

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
    context = "\n".join([doc[0].page_content for doc in past_entries])  # doc[0] is Document

    # Step 3: Build prompt
    prompt = f"""
    You are a reflective journaling assistant.
    User just wrote: "{user_input}".
    Sentiment detected: {sentiment}.
    Here are related past entries:
    {context}

    Based on this, give an empathetic reflection.
    Suggest patterns, insights, or advice if relevant.
    Keep it brief and journal-friendly: 3–4 sentences, under 90 words.
    """

    # Step 4: Get response from Hugging Face LLM
    try:
        raw_response = llm(prompt)
        print(f"[DEBUG] Raw LLM response: {raw_response}")  # For debugging
        # Handle different output formats
        def extract_text(resp):
            if isinstance(resp, list) and len(resp) > 0:
                item = resp[0]
                if isinstance(item, dict):
                    for key in item:
                        if isinstance(item[key], str):
                            return item[key]
                    return str(item)
                elif isinstance(item, str):
                    return item
                else:
                    return str(item)
            elif isinstance(resp, dict):
                for key in resp:
                    if isinstance(resp[key], str):
                        return resp[key]
                return str(resp)
            elif isinstance(resp, str):
                return resp
            else:
                return str(resp)
        return extract_text(raw_response)
    except Exception as e:
        # Catch errors like API key issues
        return f"[ERROR] LLM failed: {str(e)}"
