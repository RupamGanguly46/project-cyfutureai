def fuse_sentiments(text_sentiment, audio_sentiment):
    # Rule-based priority: anger > sadness > happiness > neutral
    priority = {"angry": 3, "sad": 2, "happy": 1, "neutral": 0, "positive": 1, "negative": 2}

    # Use whichever is stronger
    if audio_sentiment and priority[audio_sentiment] > priority.get(text_sentiment, 0):
        return audio_sentiment
    return text_sentiment or "neutral"
