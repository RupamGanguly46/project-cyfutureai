from pyAudioAnalysis import audioSegmentation as aS

def analyze_audio_emotion(audio_path):
    try:
        flags, _, _ = aS.mtFileClassification(audio_path, "pyAudioAnalysis/data/svmSpeechEmotion", "svm")
        # Map numerical prediction to emotion
        mapping = {0: "neutral", 1: "happy", 2: "sad", 3: "angry"}
        return mapping.get(flags[0], "neutral")
    except:
        return "neutral"
