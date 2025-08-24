import streamlit as st
from utils.export_helpers import save_results
from utils.language_helpers import detect_language
from utils.llm_helpers import summarize, estimate_cost
from utils.tokenizer_helpers import tokenize, visualize_boundaries, token_count

st.set_page_config(page_title="LLM Summarizer & Token Explorer", layout="wide")
st.title("🧠 LLM Summarizer + Tokenization Explorer")

# Input text
text = st.text_area("Enter text to summarize")

# Model selection (Gemini or Claude)
model_choice = st.selectbox("Choose a model", ["Google Gemini", "Anthropic Claude"])

if st.button("Summarize with LLM"):
    if not text.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        # Language Detection
        lang_info = detect_language(text)
        st.subheader("🌍 Language Detection")
        st.write(f"**Detected Language:** {lang_info['language']}")
        if lang_info["probabilities"]:
            st.write("**Probabilities:**", lang_info["probabilities"])

        # Summarization
        summary = summarize(text, model_choice)
        st.subheader("📄 Summary")
        st.write(summary)

        # Token stats
        input_tokens = token_count(text)
        output_tokens = token_count(summary)
        st.subheader("📊 Token Usage")
        st.write(f"**Input tokens:** {input_tokens}")
        st.write(f"**Output tokens:** {output_tokens}")

        # Cost estimate
        cost = estimate_cost(input_tokens, output_tokens, model_choice)
        st.write(f"💰 Estimated Cost: **${cost}**")

        # Tokenization breakdown
        st.subheader("🔤 Tokenization Breakdown")

        # GPT Tokenization
        gpt_tokens = tokenize(text, model="gpt")
        with st.expander("Show GPT Tokenization Details"):
            st.markdown("### 🔹 GPT Tokenization")
            st.write("**Tokens:**", gpt_tokens["tokens"])
            st.write(f"**Token Count:** {gpt_tokens['token_count']}")
            st.write(f"**Unique Tokens:** {gpt_tokens['unique_tokens']}")
            st.write(f"**Average Token Length:** {gpt_tokens['avg_token_length']}")
            st.markdown(visualize_boundaries(gpt_tokens["boundaries"]))

        # BERT Tokenization
        bert_tokens = tokenize(text, model="bert")
        with st.expander("Show BERT Tokenization Details"):
            st.markdown("### 🔹 BERT Tokenization")
            st.write("**Tokens:**", bert_tokens["tokens"])
            st.write(f"**Token Count:** {bert_tokens['token_count']}")
            st.write(f"**Unique Tokens:** {bert_tokens['unique_tokens']}")
            st.write(f"**Average Token Length:** {bert_tokens['avg_token_length']}")
            st.markdown(visualize_boundaries(bert_tokens["boundaries"]))
        
        save_results({
        "model": model_choice,
        "input_text": text,
        "summary": summary,
        "language": lang_info["language"],
        "probabilities": lang_info["probabilities"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": cost,
        "gpt_tokens": gpt_tokens,
        "bert_tokens": bert_tokens
        }, file_path="data/results/result.json")

