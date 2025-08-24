from transformers import AutoTokenizer
import matplotlib.pyplot as plt
from collections import Counter
from typing import Dict, List, Tuple

# Load common tokenizers
gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2")                # GPT approximation
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # BERT

def tokenize(text: str, model: str = "gpt") -> Dict:
    """
    Tokenize text using GPT or BERT and return token boundaries + stats.
    """
    if not text.strip():
        return {
            "tokens": [],
            "token_count": 0,
            "unique_tokens": 0,
            "avg_token_length": 0,
            "model": model,
            "boundaries": []
        }

    if model == "gpt":
        tokens = gpt_tokenizer.encode(text)
        decoded_tokens = [gpt_tokenizer.decode([t]) for t in tokens]

    elif model == "bert":
        tokens = bert_tokenizer.tokenize(text)
        decoded_tokens = tokens  # already strings

    else:
        raise ValueError("Unsupported model. Use 'gpt' or 'bert'.")

    # Stats
    token_count = len(decoded_tokens)
    unique_tokens = len(set(decoded_tokens))
    avg_token_length = sum(len(t) for t in decoded_tokens) / token_count

    return {
        "tokens": decoded_tokens,
        "token_count": token_count,
        "unique_tokens": unique_tokens,
        "avg_token_length": round(avg_token_length, 2),
        "model": model,
        "boundaries": [(i, tok) for i, tok in enumerate(decoded_tokens)]
    }


def token_count(text: str, model: str = "gpt") -> int:
    """Return number of tokens for a given text."""
    return len(tokenize(text, model))

def compare_tokenization(text: str) -> dict:
    """Compare GPT vs BERT tokenization of the same text."""
    return {
        "gpt_tokens": gpt_tokenizer.tokenize(text) if text.strip() else [],
        "bert_tokens": bert_tokenizer.tokenize(text) if text.strip() else []
    }

def token_statistics(tokens: list) -> dict:
    """Calculate statistics from a token list."""
    if not tokens:
        return {"total_tokens": 0, "avg_length": 0, "unique_tokens": 0, "freq": {}}
    
    lengths = [len(t) for t in tokens]
    counter = Counter(tokens)
    return {
        "total_tokens": len(tokens),
        "avg_length": sum(lengths) / len(tokens),
        "unique_tokens": len(set(tokens)),
        "freq": counter.most_common(5)  # top 5 frequent tokens
    }

def visualize_tokens(text: str):
    """Visualize token boundaries for GPT and BERT using matplotlib."""
    comp = compare_tokenization(text)
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 4))
    fig.suptitle("Tokenization Comparison")
    
    # GPT tokens
    axs[0].bar(range(len(comp["gpt_tokens"])), [len(t) for t in comp["gpt_tokens"]])
    axs[0].set_title("GPT Tokens")
    axs[0].set_xticks(range(len(comp["gpt_tokens"])))
    axs[0].set_xticklabels(comp["gpt_tokens"], rotation=45, ha="right")
    
    # BERT tokens
    axs[1].bar(range(len(comp["bert_tokens"])), [len(t) for t in comp["bert_tokens"]])
    axs[1].set_title("BERT Tokens")
    axs[1].set_xticks(range(len(comp["bert_tokens"])))
    axs[1].set_xticklabels(comp["bert_tokens"], rotation=45, ha="right")
    
    plt.tight_layout()
    plt.show()

def visualize_boundaries(boundaries: List[Tuple[int, str]]) -> str:
    """
    Create a simple visualization of token boundaries.
    """
    return " | ".join([f"[{i}:{tok}]" for i, tok in boundaries])