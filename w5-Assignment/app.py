import streamlit as st

st.write("DEBUG: st.secrets dict →", st.secrets)

if "GEMINI_API_KEY" in st.secrets:
    st.success(f"GEMINI_API_KEY found! Value starts with: {st.secrets['GEMINI_API_KEY'][:5]}*****")
else:
    st.error("GEMINI_API_KEY is missing from secrets!")
