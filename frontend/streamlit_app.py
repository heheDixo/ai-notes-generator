import streamlit as st
import requests

st.set_page_config(page_title="AI YouTube Smart Notes", layout="wide")

st.title("🎓 AI YouTube Smart Notes")
st.write("Paste a YouTube link and get beautiful revision notes.")

url = st.text_input("YouTube URL")

if st.button("Generate Notes"):
    if url:
        with st.spinner("Generating notes... This may take 30-40 seconds"):
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/generate-notes",
                    json={"url": url},
                    timeout=120
                )
                data = res.json()
                st.write(data)  # show full response

            except Exception as e:
                st.error(f"Error: {e}")