from langchain_core.messages import HumanMessage
import os
PROMPTS_BASE_DIR = os.path.join(os.path.dirname(__file__), "prompts")

# Load system prompt content from a file
def systemPromptContentLoader (persona_file_name: str) -> str:
    file_path = os.path.join(PROMPTS_BASE_DIR, persona_file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error loading prompt '{persona_file_name}' from {file_path}: {e}. Using a default prompt.")
        return "you are a default prompt."

# Generate AI response for chat
def aiResponseForChat(
        current_chat_history: list,
        model_instance,
        user_query: str
) -> str:
    """
    process the user query and generate a response using the model instance
    """
    temp_chat_history = list(current_chat_history)
    temp_chat_history.append = (HumanMessage(content=user_query))

    formatted_prompt = " ".join(str(msg.content) for msg in temp_chat_history)
    try:
        response = model_instance.gemini_chat_models(formatted_prompt)
        return response
    except Exception as e:
        return "An error occurred while generating a response."

if __name__ == "__main__":
    print("This is the core of this project's model. Please run the streamlit app for the web UI.")