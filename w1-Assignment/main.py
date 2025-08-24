# main.py

import argparse
import json
from utils.llm_helpers import summarize, estimate_cost
from utils.tokenizer_helpers import token_count


def main():
    parser = argparse.ArgumentParser(description="Text Analysis Tool (Gemini + DeepSeek)")
    parser.add_argument("--task", choices=["summarize"], required=True,
                        help="Task to perform (currently only: summarize)")
    parser.add_argument("--model", choices=["gemini", "deepseek"], required=True,
                        help="Which model to use")
    parser.add_argument("--file", type=str, required=True,
                        help="Path to input text file")
    parser.add_argument("--save", action="store_true",
                        help="Save results to JSON file in data/results/")

    args = parser.parse_args()

    # Load input text
    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    if args.task == "summarize":
        print(f"\n📝 Running summarization with {args.model}...\n")
        summary = summarize(text, args.model)

        # Token counts
        input_tokens = token_count(text)
        output_tokens = token_count(summary)
        est_cost = estimate_cost(input_tokens, output_tokens, args.model)

        # Print results
        print("=== SUMMARY ===")
        print(summary)
        print("\n=== STATS ===")
        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Estimated cost: ${est_cost}")

        # Save results
        if args.save:
            results = {
                "model": args.model,
                "input_file": args.file,
                "summary": summary,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "estimated_cost": est_cost,
            }
            out_path = f"data/results/{args.model}_summary.json"
            with open(out_path, "w", encoding="utf-8") as out_f:
                json.dump(results, out_f, indent=4, ensure_ascii=False)
            print(f"\n✅ Results saved to {out_path}")


if __name__ == "__main__":
    main()
