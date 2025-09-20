from src.utils.llm_setup import llm
from src.utils.db import search_entries
from src.tools.sentiment import analyze_sentiment

def reflect(db, user_input):
    # Step 1: Sentiment of new entry
    sentiment = analyze_sentiment
    
    # Step 2: Retrieve similar past entries
    past_entries = search_entries(db, user_input, k=3)
    context = "\n".join([doc.page_content for doc in past_entries])
    
    # Step 3: Build Prompt
    prompt = f"""
    You are a reflective journaling assistant.
    User just wrote: :{user_input}".
    Sentiment detected: {sentiment}.
    Here are related past entries:
    {context}
    
    Based on this, give an empathetic reflection.
    Suggest patterns or insight if relevant.
    """
    
    # Step 4: Get response from Gemini
    response = llm.invoke(prompt)
    return response.content