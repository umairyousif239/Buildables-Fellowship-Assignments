import google.generativeai as genai

class ChatModel:
    """
    A class to interact with the Google Generative AI API for chat-based tasks
    """

    def __init__(self, gemini_api: str | None = None) -> None:
        self.gemini_api = gemini_api
        if self.gemini_api is None:
            print("Warning: Gemini API Key is missing.")
        else:
            genai.configure(api_key=self.gemini_api)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
            self.chat = self.model.start_chat(history=[])

    def gemini_chat_models(self, prompt: str) -> str:
        """
        Sends the prompt to the Gemini chat model and returns a response.
        """
        try:
            response = self.chat.send_message(prompt)
            content = response.text
            return content.strip() if content else "No response content."
        except Exception as e:
            return f"An error occurred with the Gemini chat model: {e}"