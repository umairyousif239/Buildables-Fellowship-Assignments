import google.generativeai as genai
import config

# Setup Gemini
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def summarize_article(article, length, persona):
    style = persona.get("style", "")
    temperature = persona.get("temperature", 0.7)

    prompt = f"""
    {style}
    Summarize the following article in a {length} way:
    
    {article}
    """

    response = model.generate_content(
        prompt,
        generation_config={"temperature": temperature, "max_output_tokens": 400},
    )
    return response.text


def ask_question(article, question, persona):
    style = persona.get("style", "")
    temperature = persona.get("temperature", 0.7)

    prompt = f"""
    {style}
    Based on the following article, answer the question below.

    Article:
    {article}

    Question:
    {question}
    """

    response = model.generate_content(
        prompt,
        generation_config={"temperature": temperature, "max_output_tokens": 400},
    )
    return response.text
