# from pyAudioAnalysis import audioSegmentation as aS

# def analyze_audio_emotion(audio_path):
#     try:
#         flags, _, _ = aS.mtFileClassification(audio_path, "pyAudioAnalysis/data/svmSpeechEmotion", "svm")
#         mapping = {0: "neutral", 1: "happy", 2: "sad", 3: "angry"}
#         return mapping.get(flags[0], "neutral")
#     except:
#         return "neutral"

from transformers import pipeline
dictio = {"ang":"angry", "hap":"happy", "neu":"neutral", "sad":"sad"}
emotion_pipeline = pipeline(task="audio-classification", model="superb/wav2vec2-base-superb-er")

def analyze_audio_emotion(audio_path):

    result = emotion_pipeline(f"{audio_path}")
    # result: list of dicts like [{'score': 0.99, 'label': 'ang'}, ...]

    sorted_scores = sorted(result, key=lambda x: x['score'], reverse=True)
    top = sorted_scores[0]
    if top['label'] == 'neu' and len(sorted_scores) > 1:
        # If next best is close (within 10%), prefer it over neutral
        if sorted_scores[1]['score'] >= 0.9 * top['score']:
            return sorted_scores[1]['label']
    return dictio[top['label']]