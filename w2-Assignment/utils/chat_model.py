import google.generativeai as genai

# ChatModel class
class ChatModel:
    """
    a class to interact with the Google Generative AI API for chat-based tasks
    """

    # Initialize the ChatModel with the provided Gemini API key.
    def __init__(self, gemini_api: str | None = None) -> None:
        """
        Initialize the ChatModel with the provided Gemini API key.
        """
        self.gemini_api = gemini_api
        if self.gemini_api is None:
            print("Warning: Gemini API Key is missing.")

    # Interact with the Gemini chat model.
    def gemini_chat_models(self, prompt: str) -> str:
        """
        Sends the prompt to the Gemini chat model and returns a response.
        """
        try:
            genai.configure(api_key=self.gemini_api)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_message(prompt)
            content = response.text
            return content.strip() if content is not None else "No response content."
        except Exception as e:
            return f"An error occurred with the Gemini chat model: {e}"