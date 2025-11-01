from langdetect import detect, detect_langs

def detect_language(text: str):
    try:
        lang = detect(text)
        probabilities = detect_langs(text)  # gives a list with probabilities
        return {
            "language": lang,
            "probabilities": {str(p.lang): p.prob for p in probabilities}
        }
    except Exception:
        return {"language": "unknown", "probabilities": {}}
