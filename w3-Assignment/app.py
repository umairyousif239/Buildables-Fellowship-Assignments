from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from model_core import systemPromptContentLoader
from utils.chat_model import ChatModel
import streamlit as st
import config
import os

# Prompts directory
_PROMPTS_ABS_DIR_ = os.path.join(os.path.dirname(__file__), "prompts")

if not os.path.exists(_PROMPTS_ABS_DIR_):
    os.makedirs(_PROMPTS_ABS_DIR_)
    st.warning(f"Created missing prompt directory: {_PROMPTS_ABS_DIR_}")

# Get available personas
def get_available_personas() -> list[str]:
    """
    Scans the prompts directory and returns a list of available persona names.
    """
    persona_files = [f for f in os.listdir(_PROMPTS_ABS_DIR_) if f.endswith('.txt')]
    return [os.path.splitext(f)[0].replace('_', ' ').title() for f in persona_files]

# Export chat history as text
def export_chat_history_as_text():
    """
    Formats the chat history for export as plain text.
    """
    export_string = ""
    for message in st.session_state.chat_history:
        if isinstance(message, SystemMessage):
            export_string += f"System: {message.content}\n"
        elif isinstance(message, HumanMessage):
            export_string += f"You: {message.content}\n"
        elif isinstance(message, AIMessage):
            export_string += f"Assistant: {message.content}\n"
    return export_string

# Streamlit app configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("Gemini Chatbot")
st.markdown("### A chatbot powered by Google Gemini-2.0-flash model built for the Buildables Internship.")
st.markdown("---")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "system_prompt_content" not in st.session_state:
    st.session_state.system_prompt_content = ""

# Initialize model
if "model" not in st.session_state:
    try:
        st.session_state.model = ChatModel(gemini_api=config.GEMINI_API_KEY)
    except AttributeError:
        st.warning("Gemini API key is missing. Falling back to environment variables.")
        gemini_api = os.getenv("GEMINI_API_KEY")
        st.session_state.model = ChatModel(gemini_api)
if st.session_state.model.gemini_api is None:
    st.error("Gemini API key is missing. Please set it in config.py or as an environment variable.")
    st.stop()

st.sidebar.header("Chat Settings")

# Persona Selector
available_personas = get_available_personas()
if "Professional Assistant" in available_personas:
    default_persona_index = available_personas.index("Professional Assistant")
elif available_personas:
    default_persona_index = 0
else:
    default_persona_index = -1

# Persona Fallback
if default_persona_index == -1:
    st.warning("No persona prompt files found. using default assistant.")
    selected_persona_display_name = "Default Assistant"
else:
    selected_persona_display_name = st.sidebar.selectbox(
        "Choose AI Persona:",
        options=available_personas,
        index=default_persona_index,
        key="persona_selector"
    )

# Format selected persona display name
selected_persona_display_name = selected_persona_display_name.lower().replace(' ', '_') + ".txt" if selected_persona_display_name != "Default Assistant" else ""

# Load system prompt content
new_system_prompt_content = systemPromptContentLoader(selected_persona_display_name) if selected_persona_display_name else "You are a default assistant."

# Update session state if system prompt content has changed
if st.session_state.system_prompt_content != new_system_prompt_content:
    st.session_state.system_prompt_content = new_system_prompt_content
    st.session_state.chat_history = []
    st.rerun()

# Update chat history if system prompt content has changed
if not st.session_state.chat_history or not isinstance(st.session_state.chat_history[0], SystemMessage) or st.session_state.chat_history[0].content != st.session_state.system_prompt_content:
    st.session_state.chat_history = [SystemMessage(content=st.session_state.system_prompt_content)] + \
                                    [msg for msg in st.session_state.chat_history if not isinstance(msg, SystemMessage)]

# Update chat history if system prompt content has changed
st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat History", key="clear_chat_button"):
    st.session_state.chat_history = [SystemMessage(content=st.session_state.system_prompt_content)]
    st.rerun()

# Export chat history
st.sidebar.download_button(
    label="Export Chat History",
    data=export_chat_history_as_text(),
    file_name="chat_history.txt",
    mime="text/plain",
    key="export_chat_button"
)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by [Umair Yousif](https://www.linkedin.com/in/umairyousif) | [GitHub](https://github.com/umairyousif239)")
st.sidebar.markdown("Powered by [Google Gemini-2.0-flash](https://developers.generativeai.google/products/gemini) | [Buildables Fellowship](https://buildables.dev/#/fellowship)")

# Chat History
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content.replace("$","\$"))
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content.replace("$","\$"))

# User Input
if user_query := st.chat_input("Type your message here.", key="user_input"):
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("user"):
        st.write(user_query.replace("$","\$"))

    with st.spinner("Thinking..."):
        try:
            formatted_prompt = ' '.join(
                str(msg.content) for msg in st.session_state.chat_history
            )
            if st.session_state.model.gemini_api is None:
                ai_response_text = "Error: Gemini API key is not set. Please check your config.py or environment variables."
            else:
                ai_response_text = st.session_state.model.gemini_chat_models(formatted_prompt)
            
            st.session_state.chat_history.append(AIMessage(content=ai_response_text))
            with st.chat_message("assistant"):
                st.write(ai_response_text.replace("$","\$"))
        except Exception as e:
            st.error(f"Error from the AI model: {e}")
            if len(st.session_state.chat_history) > 1:
                st.session_state.chat_history.pop()