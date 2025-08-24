from transformers import AutoTokenizer

# Common tokenizers
gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2")           # approximation for GPT/Gemini
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # for comparison


def tokenize(text: str, model: str = "gpt") -> list:
    """Tokenize text with chosen model tokenizer."""
    if model == "gpt":
        return gpt_tokenizer.encode(text)
    elif model == "bert":
        return bert_tokenizer.encode(text)
    else:
        raise ValueError(f"Unsupported tokenizer: {model}")


def token_count(text: str, model: str = "gpt") -> int:
    """Return number of tokens for a given text."""
    return len(tokenize(text, model))


def compare_tokenization(text: str) -> dict:
    """Compare GPT vs BERT tokenization of the same text."""
    return {
        "gpt_tokens": gpt_tokenizer.tokenize(text),
        "bert_tokens": bert_tokenizer.tokenize(text)
    }