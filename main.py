# from fastapi import FastAPI, Request, UploadFile, File, Form
# from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import os
# import uuid

# from audio_transcriber import transcribe_audio
# from text_sentiment import analyze_text_sentiment
# from audio_sentiment import analyze_audio_emotion
# from fusion_logic import fuse_sentiments
# from llm_chain import get_response
# from database import insert_chat
# from tts_response import generate_tts
# from chat_memory import memory

# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Create uploads directory once
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.post("/chat/")
# async def chat_endpoint(text: str = Form(None), file: UploadFile = File(None)):
#     user_input = ""
#     audio_sentiment = None

#     if file:
#         file_ext = os.path.splitext(file.filename)[1]
#         unique_filename = f"{uuid.uuid4().hex}{file_ext}"
#         file_path = os.path.join(UPLOAD_DIR, unique_filename)

#         contents = await file.read()
#         with open(file_path, "wb") as f:
#             f.write(contents)

#         user_input = transcribe_audio(file_path)
#         audio_sentiment = analyze_audio_emotion(file_path)

#     else:
#         # If no audio, use text input directly
#         if not text:
#             return JSONResponse({"error": "No text or audio file provided"}, status_code=400)
#         user_input = text
    
#     # Analyze text sentiment
#     text_sentiment = analyze_text_sentiment(user_input)

#     # Fuse text and audio sentiments
#     sentiment = fuse_sentiments(text_sentiment, audio_sentiment)

#     print(f"{audio_sentiment=},{text_sentiment=},{sentiment=}")

#     # Get LLM response with chat memory
#     response = get_response(user_input, sentiment)

#     # Generate TTS audio file path
#     tts_path = generate_tts(response)

#     # Insert chat record in DB
#     # insert_chat(user_input, response, sentiment)

#     try:
#         insert_chat(user_input, response, sentiment)
#     except Exception as e:
#         logger.error(f"DB insert failed: {e}")


#     # Return response and TTS audio path (frontend should request /static or a separate route)
#     return JSONResponse({
#         "response": response,
#         "audio_path": tts_path,
#         "user_audio_path": os.path.basename(file_path) if file else None
#     })

# import warnings
# warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

# from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
# from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import os
# import uuid
# import logging
# from dotenv import load_dotenv

# from audio_transcriber import transcribe_audio
# from text_sentiment import analyze_text_sentiment
# from audio_sentiment import analyze_audio_emotion
# from fusion_logic import fuse_sentiments
# from llm_chain import get_response
# from database import insert_chat
# from tts_response import generate_tts
# from chat_memory import memory

# # Load environment variables
# load_dotenv()

# # Logging setup
# LOG_FILE = "chatbot.log"
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s",
#     handlers=[
#         logging.FileHandler(LOG_FILE),  # Save to file
#         logging.StreamHandler()         # Also show in terminal (controlled below)
#     ]
# )
# logger = logging.getLogger("customer-support-app")

# # Suppress uvicorn and other noisy loggers except critical errors
# logging.getLogger("uvicorn").setLevel(logging.ERROR)
# logging.getLogger("uvicorn.error").setLevel(logging.ERROR)
# logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
# logging.getLogger("httpx").setLevel(logging.WARNING)
# logging.getLogger("asyncio").setLevel(logging.WARNING)

# # Create uploads directory once
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# templates = Jinja2Templates(directory="templates")

# MAX_UPLOAD_SIZE_MB = 10
# @app.middleware("http")
# async def limit_upload_size(request: Request, call_next):
#     if "content-length" in request.headers:
#         content_length = int(request.headers["content-length"])
#         if content_length > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
#             raise HTTPException(status_code=413, detail="File too large")
#     return await call_next(request)


# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/chat/")
# async def chat_endpoint(text: str = Form(None), file: UploadFile = File(None)):
#     user_input = ""
#     audio_sentiment = None
#     file_path = None  # define here for scope

#     try:
#         if file:
#             file_ext = os.path.splitext(file.filename)[1]
#             unique_filename = f"{uuid.uuid4().hex}{file_ext}"
#             file_path = os.path.join(UPLOAD_DIR, unique_filename)

#             contents = await file.read()
#             with open(file_path, "wb") as f:
#                 f.write(contents)

#             user_input = transcribe_audio(file_path)
#             audio_sentiment = analyze_audio_emotion(file_path)
#         else:
#             if not text:
#                 return JSONResponse({"error": "No text or audio file provided"}, status_code=400)
#             user_input = text

#         # Analyze text sentiment
#         text_sentiment = analyze_text_sentiment(user_input)

#         # Fuse text and audio sentiments
#         sentiment = fuse_sentiments(text_sentiment, audio_sentiment)

#         # Get LLM response with chat memory
#         response = get_response(user_input, sentiment)

#         # Generate TTS audio file path
#         tts_path = generate_tts(response)

#         # Log the user input
#         logger.info(f"{user_input=}")
#         logger.info(f"{audio_sentiment=},{text_sentiment=},{sentiment=}")
#         logger.info(f"{response=}")
#         logger.info(f"{tts_path=}")

#         # Insert chat record in DB
#         try:
#             insert_chat(user_input, response, sentiment)
#         except Exception as e:
#             logger.error(f"DB insert failed: {e}")

#         return JSONResponse({
#             "response": response,
#             "audio_path": tts_path,
#             "user_audio_path": os.path.basename(file_path) if file else None
#         })

#     except Exception as e:
#         logger.error(f"Error handling chat request: {e}", exc_info=True)
#         return JSONResponse({"error": "Internal server error"}, status_code=500)

# if __name__ == "__main__":
#     logger.info("Server is starting...")
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="error")
#     logger.info("Server stopped.")

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uuid
import logging
from dotenv import load_dotenv
import sys
import io

from audio_transcriber import transcribe_audio
from text_sentiment import analyze_text_sentiment
from audio_sentiment import analyze_audio_emotion
from fusion_logic import fuse_sentiments
from llm_chain import get_response
from database import insert_chat
from tts_response import generate_tts
from chat_memory import memory

# --- UTF-8 stdout for terminal (especially for Windows) ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# Logging setup
LOG_FILE = "chatbot.log"

# Remove default handlers if re-running in environments like Jupyter or Uvicorn
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Set up only our custom logger
logger = logging.getLogger("customer-support-app")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent duplicate logs

# File handler
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Stream handler for terminal
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Suppress all other loggers
for log_name in logging.root.manager.loggerDict:
    if log_name != "customer-support-app":
        logging.getLogger(log_name).setLevel(logging.CRITICAL)

# Create uploads directory once
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In order to log server start and stop
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Server has started.")
    yield
    logger.info("🛑 Server has stopped.")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

MAX_UPLOAD_SIZE_MB = 10

@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if "content-length" in request.headers:
        content_length = int(request.headers["content-length"])
        if content_length > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large")
    return await call_next(request)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# TO FORMAT TEXT AND REMOVE MARKDOWN SYNTAX FROM OUTPUT
import re
def clean_response_for_user(text):
    """Clean LLM response minimally - only remove markdown syntax, keep structure"""
    
    # Remove markdown headers but keep text and structure
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Remove bold/italic markers but keep text
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Keep list structure but remove markdown markers
    text = re.sub(r'^[-*+]\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # Keep [text](url) for frontend processing
    
    # Minimal whitespace cleanup - preserve most structure
    text = re.sub(r'\n{4,}', '\n\n\n', text)  # Max 3 consecutive newlines
    
    return text.strip()

@app.post("/chat/")
async def chat_endpoint(text: str = Form(None), file: UploadFile = File(None)):
    user_input = ""
    audio_sentiment = None
    file_path = None  # define here for scope

    try:
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
            if not text:
                return JSONResponse({"error": "No text or audio file provided"}, status_code=400)
            user_input = text

        # Analyze text sentiment
        text_sentiment = analyze_text_sentiment(user_input)

        # Fuse text and audio sentiments
        sentiment = fuse_sentiments(text_sentiment, audio_sentiment)

        # # Get LLM response with chat memory
        # response = get_response(user_input, sentiment)

        # # Generate TTS audio file path
        # tts_path = generate_tts(response)

        # New lines for new database
        import time
        start_time = time.time()
        response = get_response(user_input, sentiment)

        # Clean the response for user display (remove markdown but keep links)
        clean_response = clean_response_for_user(response)

        # tts_path = generate_tts(response)
        tts_path = generate_tts(clean_response)
        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)

        # Log only your custom info
        logger.info(f"{user_input=}")
        logger.info(f"{audio_sentiment=},{text_sentiment=},{sentiment=}")
        logger.info(f"{response=}")
        logger.info(f"{tts_path=}")

        try:
            insert_chat(
                user_input=user_input,
                bot_response=response,
                text_sentiment=text_sentiment,
                audio_sentiment=audio_sentiment,
                fused_sentiment=sentiment,
                user_audio_path=os.path.basename(file_path) if file else None,
                tts_audio_path=os.path.basename(tts_path),
                response_time_ms=response_time_ms,
                session_id="session_xyz",  # You can generate or assign real session IDs later
                intent="unknown"  # Placeholder – you can run a basic intent classifier
            )
        except Exception as e:
            logger.error(f"DB insert failed: {e}")

        # # Insert chat record in DB
        # try:
        #     insert_chat(user_input, response, sentiment)
        # except Exception as e:
        #     logger.error(f"DB insert failed: {e}")

        return JSONResponse({
            "response": clean_response,
            "audio_path": tts_path,
            "user_audio_path": os.path.basename(file_path) if file else None
        })

    except Exception as e:
        logger.error(f"Error handling chat request: {e}", exc_info=True)
        return JSONResponse({"error": "Internal server error"}, status_code=500)

# uvicorn main:app --host 0.0.0.0 --port 8000 --log-level critical --reload
