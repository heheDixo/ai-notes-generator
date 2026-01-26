from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.transcript import extract_video_id, get_transcript_with_lang
from app.services.chunking import chunk_text
from app.services.llm import get_llm
from app.services.notes import generate_notes_from_chunks


app = FastAPI(title="AI YouTube Smart Notes (Gemini V1)")

llm = get_llm()


class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "AI YouTube Smart Notes API is running"}

@app.post("/generate-notes")
def generate_notes(video: VideoRequest):
    try:
        url = video.url
        video_id = extract_video_id(url)

        # Step 1 — Get transcript from captions
        text, lang = get_transcript_with_lang(video_id)

        if not text:
            raise Exception("No captions available for this video.")

        # Step 2 — Smart semantic chunking
        chunks = chunk_text(text)

        notes = generate_notes_from_chunks(llm, chunks)

        return {"notes": notes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))