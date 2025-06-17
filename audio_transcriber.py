# import whisper

# model = whisper.load_model("base")

# def transcribe_audio(audio_path):
#     result = model.transcribe(audio_path)
#     return result["text"]

    
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

import os
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("ELEVENLABS_API_KEY")
if not apikey:
    raise ValueError("Missing Elevenlabs API Key.")

import requests

def transcribe_audio(audio_path):
    # Create transcript (POST /v1/speech-to-text)
    response = requests.post(
        "https://api.elevenlabs.io/v1/speech-to-text",
        headers={
            "Xi-Api-Key": apikey
        },
        data={
            'model_id': "scribe_v1",
        },
        files={
            'file': (os.path.basename(audio_path), open(audio_path, 'rb')),
        },
    )
    # keys = ["text", "language_code"]
    # filtered = {k: response.json().get(k) for k in keys}
    # return filtered

    return response.json()["text"]
