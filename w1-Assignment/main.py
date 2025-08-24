from utils.export_helpers import save_results
from utils.language_helpers import detect_language
from utils.llm_helpers import summarize, estimate_cost
from utils.tokenizer_helpers import token_count, tokenize, visualize_boundaries

if __name__ == "__main__":
    print("=== Text Analysis Tool ===")
    
    # Asks which model to use
    model_choice = ""
    while model_choice.lower() not in ["gemini", "deepseek"]:
        model_choice = input("Choose a model (gemini / deepseek): ").strip().lower()

    # Asks for input text
    sample_text = input("\nEnter a paragraph to summarize:\n")

    # Language Detection
    lang_info = detect_language(sample_text)
    print("\n=== LANGUAGE DETECTION ===")
    print(f"Detected: {lang_info['language']}")
    print("Probabilities:", lang_info["probabilities"])

    # Summarization
    print(f"\n📝 Running summarization with {model_choice}...\n")
    summary = summarize(sample_text, model_choice)

    # Tokenization with GPT and BERT
    for model in ["gpt", "bert"]:
        result = tokenize(sample_text, model=model)
        print(f"\n=== {model.upper()} Tokenization ===")
        print("Tokens:", result["tokens"])
        print("Token Count:", result["token_count"])
        print("Unique Tokens:", result["unique_tokens"])
        print("Avg Token Length:", result["avg_token_length"])
        print("Boundaries:", visualize_boundaries(result["boundaries"]))

    # Token counts + cost
    input_tokens = token_count(sample_text)
    output_tokens = token_count(summary)
    est_cost = estimate_cost(input_tokens, output_tokens, model_choice)
    
    run_data = {
        "model": model_choice,
        "input_text": sample_text,
        "summary": summary,
        "language": lang_info["language"],
        "probabilities": lang_info["probabilities"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": est_cost
    }

    # Save to JSON
    save_results(run_data)

    # Print results
    print("\n=== SUMMARY ===")
    print(summary)
    print("\n=== STATS ===")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Estimated cost: ${est_cost}")
