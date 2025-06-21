# WHISPER LOCAL
# import whisper

# model = whisper.load_model("base")

# def transcribe_audio(audio_path):
#     result = model.transcribe(audio_path)
#     return result["text"]

# WHISPER API
# import os
# from langchain_community.document_loaders.parsers.audio import AzureOpenAIWhisperParser
# from langchain_core.documents.base import Blob

# AZURE_API_KEY = os.getenv("AZURE_WHISPER_API_KEY")
# AZURE_ENDPOINT = os.getenv("AZURE_WHISPER_ENDPOINT")  # No trailing slash

# whisper_parser = AzureOpenAIWhisperParser(
#     api_key=AZURE_API_KEY,
#     azure_endpoint=AZURE_ENDPOINT,
#     api_version="2024-06-01",
#     deployment_name="whisper"
# )

# def transcribe_audio(audio_path):
#     audio_blob = Blob(path=audio_path)
#     response = whisper_parser.lazy_parse(audio_blob)
#     text = ""
#     for document in response:
#         text+=document.page_content + " "
#     return text

# ELEVENLABS
# import os
# from dotenv import load_dotenv

# load_dotenv()
# apikey = os.getenv("ELEVENLABS_API_KEY")
# if not apikey:
#     raise ValueError("Missing Elevenlabs API Key.")

# import requests

# def transcribe_audio(audio_path):
#     # Create transcript (POST /v1/speech-to-text)
#     response = requests.post(
#         "https://api.elevenlabs.io/v1/speech-to-text",
#         headers={
#             "Xi-Api-Key": apikey
#         },
#         data={
#             'model_id': "scribe_v1",
#         },
#         files={
#             'file': (os.path.basename(audio_path), open(audio_path, 'rb')),
#         },
#     )
#     # keys = ["text", "language_code"]
#     # filtered = {k: response.json().get(k) for k in keys}
#     # return filtered

#     return response.json()["text"]






# Language	    Code
# Assamese	    as
# Bengali	    bn
# English	    en
# Hindi	        hi
# Kannada	    kn
# Gujarati	    gu
# Malayalam	    ml
# Marathi	    mr
# Odia	        or
# Punjabi	    pa
# Tamil	        ta
# Telugu	    te

# MEGA VERSION : WHISPER + BHASHINI Lang Detect + Bhashini STT
import base64
import requests
import json
import os
from pydub import AudioSegment
import tempfile

from dotenv import load_dotenv
load_dotenv()

import whisper
model = whisper.load_model("base")
threshold=0.6

# Bhashini
api_url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"  
service_id = "bhashini/iitmandi/audio-lang-detection/gpu"
bhashini_key = os.getenv("BHASHINI_API_KEY")
if not bhashini_key:
    raise ValueError("Missing Bhashini API Key.")

indian_langs = ["as","bn","en","hi","kn","gu","ml","mr","or","pa","ta","te"]

# Sarvam
sarvam_key = os.getenv("SARVAM_API_KEY")
if not sarvam_key:
    raise ValueError("Missing Sarvam API Key.")

def detect_language_with_whisper(path, threshold=0.6):
    audio = whisper.load_audio(path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    lang, prob = max(probs.items(), key=lambda x: x[1])
    
    return lang, prob, probs

def transcribe_with_whisper(path, language):
    result = model.transcribe(path, language=language)
    return result["text"]

def transcribe_with_sarvam(path):
    # This works except assamese
    detected_lang = bhashini_detect_language(path)
    detected_lang += "-IN"

    response = requests.post(
    "https://api.sarvam.ai/speech-to-text",
    headers={
        "api-subscription-key": sarvam_key
    },
    data={
        "language_code": detected_lang
    },
    files={
        'file': (os.path.basename(path), open(path, 'rb'), 'audio/wav'),
    }
    )
    return response.json().get("transcript","")

def bhashini_detect_language(path):

    # ==== Step 1: Read and Encode Audio ====
    with open(path, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    # ==== Step 2: Build Payload ====
    payload = {
        "pipelineTasks": [
            {
                "taskType": "audio-lang-detection",
                "config": {
                    "serviceId": service_id
                }
            }
        ],
        "inputData": {
            "audio": [
                {
                    "audioContent": audio_base64
                }
            ]
        }
    }

    # ==== Step 3: Set Headers ====
    headers = {
        "Accept": "*/*",
        "Authorization": bhashini_key,
        "Content-Type": "application/json"
    }

    # ==== Step 4: Make Request ====
    response = requests.post(api_url, headers=headers, json=payload)

    # ==== Step 5: Parse Response ====
    if response.status_code == 200:
        res_json = response.json()
        try:
            lang_code = res_json["pipelineResponse"][0]["output"][0]["langPrediction"][0]["langCode"]
            print(f"🗣️ Detected Language Code by Bhashini: {lang_code}")
            return lang_code
        except Exception as e:
            print("⚠️ Failed to extract language from response by Bhashini:", e)
            print("Full response:", res_json)
    else:
        print("❌ Request failed with status by Bhashini:", response.status_code)
        print("Response:", response.text)

def transcribe_audio(audio_path):

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav_path = tmp.name

    # Convert any to WAV
    audio = AudioSegment.from_file(audio_path, format=None)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(tmp_wav_path, format="wav")

    lang, prob, probs = detect_language_with_whisper(tmp_wav_path, threshold)
    
    if prob >= threshold and (lang not in indian_langs):
        print(f"[Whisper] Detected '{lang}' with high confidence ({prob:.2f}). Transcribing...")
        return transcribe_with_whisper(tmp_wav_path, lang)
    else:
        if lang in indian_langs:
            print("Indian Language Detected by Whisper. Switching to Bhashini+Sarvam")
        else:
            print(f"[Whisper] Low confidence. Switching to Bhashini+Sarvam.")
        return transcribe_with_sarvam(tmp_wav_path)

