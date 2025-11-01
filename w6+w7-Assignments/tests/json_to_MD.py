# Converts comparison_results.json (RAG vs Non‑RAG) 
# into a human‑readable Markdown table at results/comparison_table.md.

import json
import os

SRC = os.path.join("results", "comparison_results.json")
DST = os.path.join("results", "comparison_table.md")

def to_md(rows):
    lines = ["| # | Question | RAG answer | Non-RAG answer | Better? | Why |",
            "|---|----------|------------|----------------|--------|-----|"]
    for i, r in enumerate(rows, 1):
        q = (r.get("question") or "").replace("\n", " ")
        rag = (r.get("RAG_answer") or "").replace("\n", " ")
        norag = (r.get("Non_RAG_answer") or "").replace("\n", " ")
        lines.append(f"| {i} | {q} | {rag} | {norag} |  |  |")
    return "\n".join(lines)

def main():
    if not os.path.exists(SRC):
        raise FileNotFoundError(f"{SRC} not found. Run rag_pipeline.py first.")
    with open(SRC, "r", encoding="utf-8") as f:
        data = json.load(f)
    md = to_md(data)
    os.makedirs("results", exist_ok=True)
    with open(DST, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Saved markdown table to {DST}")

if __name__ == "__main__":
    main()