import argparse
from utils.chat_model import summarize_article, ask_question

# -------------------------------
# CLI Arguments
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="News Article Summarizer & Q&A with Gemini API")
    parser.add_argument("article", type=str, help="The news article text you want to summarize")
    parser.add_argument("--length", type=str, default="short",
                        choices=["short", "medium", "detailed"],
                        help="Length of summary (short, medium, detailed)")

    args = parser.parse_args()

    # Step 1: Summarize
    summary = summarize_article(args.article, args.length)
    print("\n📰 Summary:\n")
    print(summary)

    # Step 2: Interactive Q&A
    print("\n🤔 You can now ask questions about the article. Type 'exit' to quit.\n")
    while True:
        user_q = input("Your question: ")
        if user_q.lower() in ["exit", "quit", "q"]:
            print("Goodbye 👋")
            break
        answer = ask_question(args.article, user_q)
        print("\n💡 Answer:", answer)
        print()