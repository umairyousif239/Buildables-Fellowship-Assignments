import os
import sys
import json
import hashlib
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from configurations import GEMINI_API_KEY

# Use google-generativeai (matches your installed package)
import google.generativeai as genai
import joblib

# === CONFIG ===
EXTRACTED_JSON = "extracted_output/extracted_data.json"
VECTOR_STORE_DIR = "vector_store"
INDEX_FILE = os.path.join(VECTOR_STORE_DIR, "faiss_index.bin")
EMBEDDINGS_FILE = os.path.join(VECTOR_STORE_DIR, "embeddings.npy")
CHUNKS_FILE = os.path.join(VECTOR_STORE_DIR, "chunks.json")
HASH_FILE = os.path.join(VECTOR_STORE_DIR, "data_hash.txt")

# === INIT ===
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# === HASH FUNCTION ===
def compute_file_hash(filepath):
    """Compute SHA256 hash of file contents."""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# === LOAD EXTRACTED DATA ===
if not os.path.exists(EXTRACTED_JSON):
    raise FileNotFoundError(f"❌ {EXTRACTED_JSON} not found. Run pdf_extraction.py first.")

current_hash = compute_file_hash(EXTRACTED_JSON)
stored_hash = open(HASH_FILE).read().strip() if os.path.exists(HASH_FILE) else None

# === If data unchanged, load existing FAISS and embeddings ===
if stored_hash == current_hash and all(os.path.exists(f) for f in [INDEX_FILE, EMBEDDINGS_FILE, CHUNKS_FILE]):
    print("🔁 No data changes detected — loading existing FAISS index and embeddings...")
    index = faiss.read_index(INDEX_FILE)
    embeddings = np.load(EMBEDDINGS_FILE)
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        all_chunks = json.load(f)
else:
    print("🧩 Changes detected or first run — rebuilding embeddings and FAISS index...")

    with open(EXTRACTED_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = data.get("texts", [])
    tables = [json.dumps(t, ensure_ascii=False) for t in data.get("tables", [])]
    pictures = [p.get("caption", "") for p in data.get("pictures", [])]

    all_chunks = texts + tables + pictures
    print(f"✅ Loaded {len(all_chunks)} total chunks from document.")

    embeddings = embedder.encode(all_chunks, show_progress_bar=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    # Save FAISS + metadata
    faiss.write_index(index, INDEX_FILE)
    np.save(EMBEDDINGS_FILE, embeddings)
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    with open(HASH_FILE, "w") as f:
        f.write(current_hash)

    print("✅ FAISS index, embeddings, and metadata saved.")


# === RETRIEVAL ===
def retrieve_relevant_chunks(query, top_k=5):
    query_vector = embedder.encode([query])
    distances, indices = index.search(np.array(query_vector).astype("float32"), top_k)
    return [all_chunks[i] for i in indices[0]]


# === GEMINI ANSWER FUNCTION ===
def answer_question(query, use_rag=True):
    if use_rag:
        context = "\n".join(retrieve_relevant_chunks(query))
        prompt = f"Use the following document context to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}"
    else:
        prompt = f"Answer the question without document context:\n{query}"

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )
    return response.text.strip()


# === MAIN TEST ===
if __name__ == "__main__":
    questions = [
        "What is the main goal of the AI Surveillance System?",
        "Which technologies are mentioned in the proposal?",
        "What are the limitations discussed?",
        "What datasets or data sources does it use?",
        "What conclusions are drawn?"
    ]

    results = []
    for q in questions:
        print(f"\n❓ Question: {q}")
        rag_answer = answer_question(q, use_rag=True)
        no_rag_answer = answer_question(q, use_rag=False)

        results.append({
            "question": q,
            "RAG_answer": rag_answer,
            "Non_RAG_answer": no_rag_answer
        })

        print(f"💡 RAG Answer: {rag_answer[:250]}...")
        print(f"🧠 Non-RAG Answer: {no_rag_answer[:250]}...")

    os.makedirs("results", exist_ok=True)
    with open("results/comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print("\n✅ Comparison results saved to results/comparison_results.json")