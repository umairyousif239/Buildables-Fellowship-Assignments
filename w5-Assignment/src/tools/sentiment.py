from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer

def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    if scores["compound"] >= 0.05:
        return "positive"
    elif scores["compound"] <= -0.05:
        return "negative"
    else:
        return "neutral"