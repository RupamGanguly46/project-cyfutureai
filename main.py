from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uuid


from audio_transcriber import transcribe_audio
from text_sentiment import analyze_text_sentiment
from audio_sentiment import analyze_audio_emotion
from fusion_logic import fuse_sentiments
from llm_chain import get_response
from database import insert_chat
from tts_response import generate_tts
from chat_memory import memory

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory once
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat/")
async def chat_endpoint(text: str = Form(None), file: UploadFile = File(None)):
    user_input = ""
    audio_sentiment = None

    # if file:
    #     # Validate filename to avoid issues
    #     if not file.filename:
    #         return JSONResponse({"error": "Uploaded file has no filename"}, status_code=400)

    #     file_path = os.path.join(UPLOAD_DIR, file.filename)

    #     # Save uploaded file
    #     with open(file_path, "wb") as f:
    #         f.write(await file.read())

    #     # Transcribe audio and analyze audio sentiment
    #     user_input = transcribe_audio(file_path)
    #     audio_sentiment = analyze_audio_emotion(file_path)
    if file:
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        user_input = transcribe_audio(file_path)
        audio_sentiment = analyze_audio_emotion(file_path)

    else:
        # If no audio, use text input directly
        if not text:
            return JSONResponse({"error": "No text or audio file provided"}, status_code=400)
        user_input = text

    # Analyze text sentiment
    text_sentiment = analyze_text_sentiment(user_input)

    # Fuse text and audio sentiments
    sentiment = fuse_sentiments(text_sentiment, audio_sentiment)

    # Get LLM response with chat memory
    response = get_response(user_input, sentiment)

    # Generate TTS audio file path
    tts_path = generate_tts(response)

    # Insert chat record in DB
    # insert_chat(user_input, response, sentiment)

    try:
        insert_chat(user_input, response, sentiment)
    except Exception as e:
        logger.error(f"DB insert failed: {e}")


    # Return response and TTS audio path (frontend should request /static or a separate route)
    return JSONResponse({"response": response, "audio_path": tts_path})
