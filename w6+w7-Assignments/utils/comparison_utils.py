import os
import json

def append_comparison_result(results_dir, question, rag_ans, non_rag_ans):
    os.makedirs(results_dir, exist_ok=True)
    path = os.path.join(results_dir, "comparison_results.json")
    rows = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                rows = json.load(f) or []
        except Exception:
            rows = []
    rows.append({
        "question": question,
        "RAG_answer": rag_ans,
        "Non_RAG_answer": non_rag_ans
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    return path

def export_comparison_table(results_dir):
    src = os.path.join(results_dir, "comparison_results.json")
    dst = os.path.join(results_dir, "comparison_table.md")
    if not os.path.exists(src):
        return None, "results/comparison_results.json not found."
    with open(src, "r", encoding="utf-8") as f:
        rows = json.load(f)
    lines = ["| # | Question | RAG answer | Non-RAG answer | Better? | Why |",
             "|---|----------|------------|----------------|--------|-----|"]
    for i, r in enumerate(rows, 1):
        q = (r.get("question") or "").replace("\n", " ")
        rag = (r.get("RAG_answer") or "").replace("\n", " ")
        norag = (r.get("Non_RAG_answer") or "").replace("\n", " ")
        lines.append(f"| {i} | {q} | {rag} | {norag} |  |  |")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return dst, None