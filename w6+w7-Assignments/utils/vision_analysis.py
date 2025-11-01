from PIL import Image
import google.generativeai as genai

def analyze_image(image_file, task="photograph", model_id="gemini-2.5-flash", api_key=None):
    if api_key:
        genai.configure(api_key=api_key)
    prompts = {
        "photograph": "Describe this photo in detail. Mention objects, setting, actions, and notable attributes.",
        "document": "Perform OCR and structure the text. Extract headings, sections, and key bullet points.",
        "chart": "Describe the chart and explain the trend, axes, notable data points, and insights."
    }
    model = genai.GenerativeModel(model_id)
    img = Image.open(image_file)
    resp = model.generate_content([prompts.get(task, prompts["photograph"]), img], generation_config={"temperature": 0.2})
    return resp.text.strip()