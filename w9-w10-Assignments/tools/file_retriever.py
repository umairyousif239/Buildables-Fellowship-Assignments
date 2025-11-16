# tools/file_retriever.py
def retrieve_from_file(path: str) -> str:
    # Minimal safe implementation for local testing
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "Could not read file or file not found."
