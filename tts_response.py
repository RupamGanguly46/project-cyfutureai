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

OUTPUT_DIR = "static/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_tts(text):
    lang = detect(text)
    tts = gTTS(text=text, lang=lang)

    audio_id = f"response_{uuid.uuid4().hex}.mp3"
    path = os.path.join(OUTPUT_DIR, audio_id)

    tts.save(f"{path}")
    return f"/static/audio/{audio_id}"