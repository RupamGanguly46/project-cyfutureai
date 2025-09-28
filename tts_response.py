# import pyttsx3
# import uuid
# import os

# OUTPUT_DIR = "static/audio"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# engine = pyttsx3.init()

# def generate_tts(text):
#     audio_id = f"response_{uuid.uuid4().hex}.mp3"
#     path = os.path.join(OUTPUT_DIR, audio_id)

#     engine.save_to_file(text, path)
#     engine.runAndWait()

#     return f"/static/audio/{audio_id}"

from gtts import gTTS
from langdetect import detect
import uuid
import os
import re

OUTPUT_DIR = "static/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text_for_tts(text):
    """Remove links and other formatting that shouldn't be spoken"""
    # Remove markdown links - keep only the text part
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove any remaining URLs
    text = re.sub(r'https?://[^\s]+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def generate_tts(text):
    
    # Clean the text before converting to speech
    clean_text = clean_text_for_tts(text)

    lang = detect(clean_text)
    tts = gTTS(text=clean_text, lang=lang)

    audio_id = f"response_{uuid.uuid4().hex}.mp3"
    path = os.path.join(OUTPUT_DIR, audio_id)

    tts.save(f"{path}")
    return f"/static/audio/{audio_id}"