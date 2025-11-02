import streamlit as st
import requests
import google.generativeai as genai
import json
import os
from datetime import datetime

# Config
st.set_page_config(page_title="MCP GitHub Agent — Gemini Enhanced", layout="centered")

# Setup Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

DEFAULT_BACKEND = "http://127.0.0.1:8000"
BACKEND = st.secrets.get("BACKEND_URL", DEFAULT_BACKEND)
ANALYZE_ENDPOINT = f"{BACKEND.rstrip('/')}/analyze_repo"

HISTORY_FILE = "analysis_history.json"

# Session + Cache

# 🔹 Initialize session variables
if "history" not in st.session_state:
    st.session_state.history = []
if "cache" not in st.session_state:
    st.session_state.cache = {}

# Helpers

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def analyze_repo(query: str):
    # 🔹 Check cache before calling backend
    if query in st.session_state.cache:
        return st.session_state.cache[query]

    resp = requests.get(ANALYZE_ENDPOINT, params={"query": query}, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # 🔹 Store in cache
    st.session_state.cache[query] = data
    return data

def call_gemini(repo_data: dict, query: str):
    # 🔹 Check cache before calling Gemini
    if query in st.session_state.cache and "gemini_result" in st.session_state.cache[query]:
        return st.session_state.cache[query]["gemini_result"]

    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    You are a GitHub repository analysis assistant.
    Here is the repository data (commits, issues, PRs, summary):
    {json.dumps(repo_data, indent=2)}

    Please respond strictly in this JSON format:
    {{
      "reasoning": "Step-by-step reasoning of repo activity and insights.",
      "analysis": "Detailed analysis of the repository.",
      "summary": "Concise overall summary."
    }}
    """
    response = model.generate_content(prompt)
    text = response.text

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        text_clean = text.replace("```json", "").replace("```", "").strip()
        try:
            parsed = json.loads(text_clean)
        except Exception:
            parsed = {"reasoning": text, "analysis": "N/A", "summary": "N/A"}

    # 🔹 Cache Gemini output too
    if query in st.session_state.cache:
        st.session_state.cache[query]["gemini_result"] = parsed
    else:
        st.session_state.cache[query] = {"gemini_result": parsed}

    return parsed

# UI

st.title("🤖 MCP GitHub Agent (Gemini 2.5 Flash)")
st.caption("Analyze any public GitHub repo — get reasoning, analysis, and summary.")

query = st.text_input("Enter repository ```(e.g. openai/gpt-4)```:")

if st.button("Analyze"):
    if query.strip():
        repo_query = query.strip()

        with st.spinner("Fetching repository data..."):
            repo_data = analyze_repo(f"analyze {repo_query}")

        with st.spinner("Generating insights with Gemini 2.5 Flash..."):
            gemini_resp = call_gemini(repo_data, repo_query)

        reasoning = gemini_resp.get("reasoning", "No reasoning found.")
        analysis = gemini_resp.get("analysis", "No analysis found.")
        summary = gemini_resp.get("summary", "No summary found.")

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "repo_name": repo_query,
            "reasoning": reasoning,
            "analysis": analysis,
            "summary": summary
        }

        st.session_state.history.append(entry)
        save_to_history(entry)

        # Tabs Layout
        tab1, tab2, tab3 = st.tabs(["🧠 Reasoning", "📊 Analysis", "📝 Summary"])
        with tab1:
            st.markdown(reasoning)
        with tab2:
            st.markdown(analysis)
        with tab3:
            st.markdown(summary)
    else:
        st.warning("Please enter a valid repository name.")

# History Viewer

st.divider()
st.subheader("📜 Your Session History")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        with st.expander(f"🕒 {item['timestamp']} — {item['repo_name']}"):
            st.markdown(f"**Reasoning:**\n{item['reasoning']}")
            st.markdown(f"**Analysis:**\n{item['analysis']}")
            st.markdown(f"**Summary:**\n{item['summary']}")
else:
    st.info("No session analyses yet.")
