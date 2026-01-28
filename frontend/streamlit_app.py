import streamlit as st
import requests

# minor update

st.set_page_config(page_title="AI YouTube Smart Notes", layout="wide")

API_URL = "http://127.0.0.1:8000"

st.title("🎓 AI YouTube Smart Notes")
st.write("Paste a YouTube link and get revision-ready study material.")

# Session memory
if "notes" not in st.session_state:
    st.session_state.notes = None

if "url" not in st.session_state:
    st.session_state.url = None


url = st.text_input("YouTube URL")

# Step 1 — Generate Notes
if st.button("Generate Notes"):
    if url:
        with st.spinner("Generating notes..."):
            try:
                res = requests.post(
                    f"{API_URL}/generate-notes",
                    json={"url": url},
                    timeout=120
                )
                data = res.json()

                st.session_state.notes = data["notes"]
                st.session_state.url = url

            except Exception as e:
                st.error(f"Error: {e}")

# Step 2 — Show notes if present
if st.session_state.notes:
    st.subheader("📝 Study Notes")
    st.markdown(st.session_state.notes)

    col1, col2, col3 = st.columns(3)

    # Flashcards
    with col1:
        if st.button("📇 Generate Flashcards"):
            with st.spinner("Creating flashcards..."):
                res = requests.post(
                    f"{API_URL}/generate-flashcards",
                    json={"url": st.session_state.url},
                    timeout=120
                )
                cards = res.json()["flashcards"]
                st.subheader("Flashcards")
                st.text(cards)

    # PDF
    with col2:
        if st.button("📄 Download PDF"):
            res = requests.post(
                f"{API_URL}/generate-pdf",
                json={"url": st.session_state.url},
                timeout=120
            )

            st.download_button(
                label="Click to Download PDF",
                data=res.content,
                file_name="notes.pdf",
                mime="application/pdf"
            )
    
with col3:
    if st.button("🧠 Take Quiz"):
        with st.spinner("Creating quiz..."):
            res = requests.post(
                f"{API_URL}/generate-quiz",
                json={"url": st.session_state.url},
                timeout=120
            )
            quiz = res.json()["quiz"]
            st.subheader("Quiz")
            st.text(quiz)