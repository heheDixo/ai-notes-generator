from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from app.core.config import GEMINI_API_KEY

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3,
    )

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-004",
        google_api_key=GEMINI_API_KEY,
    )