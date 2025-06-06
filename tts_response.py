import pyttsx3
import uuid
import os

OUTPUT_DIR = "static/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

engine = pyttsx3.init()

def generate_tts(text):
    audio_id = f"response_{uuid.uuid4().hex}.mp3"
    path = os.path.join(OUTPUT_DIR, audio_id)

    engine.save_to_file(text, path)
    engine.runAndWait()

    return f"/static/audio/{audio_id}"
