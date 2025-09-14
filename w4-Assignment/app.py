import streamlit as st
from utils.chat_model import summarize_article, ask_question

# -------------------------------
# Persona presets (style + temp)
# -------------------------------
personas = {
    "Standard": {
        "style": "Respond in a clear, neutral, professional tone.",
        "temperature": 0.7,
    },
    "Pirate 🏴‍☠️": {
        "style": "Respond like a pirate, using pirate slang and expressions.",
        "temperature": 0.9,
    },
    "Comedian 😂": {
        "style": "Respond like a stand-up comedian, with humor and witty remarks.",
        "temperature": 1.1,
    },
    "Sports Commentator 🎙️": {
        "style": "Respond like a sports commentator, with excitement, drama, and energetic narration.",
        "temperature": 0.8,
    },
}

st.title("📰 News Article Summarizer + Q&A (Gemini API)")

# Persona selector (always visible)
persona_choice = st.radio("Choose Assistant Persona:", list(personas.keys()))
persona = personas[persona_choice]

# Init session state
if "mode" not in st.session_state:
    st.session_state.mode = "article_input"  # "article_input" or "qna"
if "article" not in st.session_state:
    st.session_state.article = None
if "summary" not in st.session_state:
    st.session_state.summary = None

# -------------------------------
# Article Input Mode
# -------------------------------
if st.session_state.mode == "article_input":
    article_text = st.text_area("Paste your article text here:", height=250)
    summary_length = st.selectbox("Choose summary length:", ["short", "medium", "detailed"])

    if st.button("Summarize Article"):
        if article_text.strip():
            summary = summarize_article(article_text, summary_length, persona)

            # Save to session state
            st.session_state.article = article_text
            st.session_state.summary = summary
            st.session_state.mode = "qna"
            st.rerun()
        else:
            st.warning("Please paste an article first!")

# -------------------------------
# Q&A Mode
# -------------------------------
elif st.session_state.mode == "qna":
    st.subheader("📝 Summary")
    st.write(st.session_state.summary)

    st.subheader("❓ Ask Questions about the Article")
    user_question = st.text_input("Your Question")
    if st.button("Get Answer"):
        if user_question.strip():
            answer = ask_question(st.session_state.article, user_question, persona)
            st.write("💡 Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

    if st.button("⬅️ Back to Article Input"):
        st.session_state.mode = "article_input"
        st.session_state.article = None
        st.session_state.summary = None
        st.rerun()
