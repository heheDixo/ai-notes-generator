from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.responses import FileResponse
from app.services.pdf import generate_notes_pdf
import uuid

from app.services.transcript import extract_video_id, get_transcript_with_lang
from app.services.chunking import chunk_text
from app.services.llm import get_llm
from app.services.notes import generate_notes_from_chunks
from app.services.flashcards import generate_flashcards
from app.services.quiz import generate_quiz
app = FastAPI(title="AI YouTube Smart Notes (Gemini V1)")

llm = get_llm()

video_cache = {}


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

        if video_id in video_cache:
            return {"notes": video_cache[video_id]}

        text, lang = get_transcript_with_lang(video_id)
        chunks = chunk_text(text)
        notes = generate_notes_from_chunks(llm, chunks)

        video_cache[video_id] = notes

        return {"notes": notes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-pdf")
def generate_pdf(video: VideoRequest):
    try:
        video_id = extract_video_id(video.url)

        if video_id not in video_cache:
            raise HTTPException(status_code=400, detail="Generate notes first.")

        notes = video_cache[video_id]

        file_path = f"/tmp/{uuid.uuid4()}.pdf"
        generate_notes_pdf(notes, file_path)

        return FileResponse(file_path, media_type="application/pdf", filename="notes.pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-flashcards")
def flashcards(video: VideoRequest):
    try:
        video_id = extract_video_id(video.url)

        if video_id not in video_cache:
            raise HTTPException(status_code=400, detail="Generate notes first.")

        notes = video_cache[video_id]
        cards = generate_flashcards(llm, notes)

        return {"flashcards": cards}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate-quiz")
def quiz(video: VideoRequest):
    try:
        video_id = extract_video_id(video.url)

        if video_id not in video_cache:
            raise HTTPException(status_code=400, detail="Generate notes first.")

        notes = video_cache[video_id]
        quiz = generate_quiz(llm, notes)

        return {"quiz": quiz}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))