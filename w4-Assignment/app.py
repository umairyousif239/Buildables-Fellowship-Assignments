import streamlit as st
import requests
from bs4 import BeautifulSoup
from utils.chat_model import summarize_article, ask_question

# -------------------------------
# Helper: Fetch article from URL
# -------------------------------
def fetch_article_from_url(url: str) -> str:
    """
    Fetch article text from a URL using requests + BeautifulSoup.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Collect all paragraphs
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        article_text = "\n".join(paragraphs)

        return article_text.strip()
    except Exception as e:
        return f"Error fetching article: {e}"


# -------------------------------
# Persona presets
# -------------------------------
personas = {
    "Default Assistant": {"style": "", "temperature": 0.7},
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

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("📰 News Article Summarizer + Q&A Using Google Gemini")

# Persona selector (always visible)
persona_choice = st.selectbox("Choose Assistant Persona:", ["Default Assistant", "Pirate 🏴‍☠️", "Comedian 😂", "Sports Commentator 🎙️"])
persona = personas[persona_choice]

# Initialize state
if "mode" not in st.session_state:
    st.session_state.mode = "article_input"

# -------------------------------
# Article Input Mode
# -------------------------------
if st.session_state.mode == "article_input":
    input_type = st.selectbox("How would you like to provide the article?", ["Paste Text", "Paste URL"])

    article_text = ""
    if input_type == "Paste Text":
        article_text = st.text_area("Paste your article text here:", height=250)

    elif input_type == "Paste URL":
        url = st.text_input("Paste the article URL here:")
        if url.strip():
            article_text = fetch_article_from_url(url)
            if article_text.startswith("Error"):
                st.error(article_text)
            else:
                st.success("✅ Article extracted successfully!")

    # Summary length choice
    summary_length = st.selectbox("Choose summary length:", ["short", "medium", "detailed"])

    # Summarization button
    if st.button("Summarize Article"):
        if article_text.strip() and not article_text.startswith("Error"):
            summary = summarize_article(article_text, summary_length, persona)
            st.session_state.article = article_text
            st.session_state.summary = summary
            st.session_state.mode = "qna"
            st.rerun()
        else:
            st.warning("Please provide either text or a valid URL.")

# -------------------------------
# Q&A Mode
# -------------------------------
elif st.session_state.mode == "qna":
    with st.expander("📝 View Summary", expanded=True):
        st.write(st.session_state.summary)

    # 📊 Show article stats
    word_count = len(st.session_state.article.split())
    estimated_tokens = int(word_count * 1.3)  # rough conversion

    with st.expander("📊 Article Stats", expanded=False):
        st.write(f"**Word count passed to summarizer:** {word_count}")
        st.write(f"**Estimated token count:** {estimated_tokens}")
        st.caption("ℹ️ Token estimate is approximate, actual usage may vary.")

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