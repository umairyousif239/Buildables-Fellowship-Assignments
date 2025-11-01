# app.py
import streamlit as st
import requests
import os

BACKEND = st.secrets.get("BACKEND_URL") or "http://localhost:8000"

st.set_page_config(page_title="MCP Agent", layout="wide")
st.title("MCP + LangGraph Agent")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Your message", key="input")

if st.button("Send") and query:
    payload = {
        "mcp_version": "1.0",
        "user_id": "test_user",
        "context": {},  # extend if you want to select files or tools
        "query": query
    }
    with st.spinner("Thinking..."):
        resp = requests.post(f"{BACKEND}/mcp", json=payload, timeout=30)
        data = resp.json()
        if not data.get("ok"):
            st.error("Error from backend")
        else:
            result = data["result"]
            st.session_state.history.append({"query": query, "result": result})

for item in reversed(st.session_state.history):
    st.markdown(f"**You:** {item['query']}")
    st.markdown(f"**Agent answer:** {item['result']['answer']}")
    st.markdown("**Trace:**")
    for step in item['result']['trace']:
        st.text(step)
    st.markdown("---")
