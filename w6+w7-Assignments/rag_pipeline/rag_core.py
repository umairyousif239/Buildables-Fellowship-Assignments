import os, json, hashlib
import numpy as np
import faiss
import sys
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from configurations import GEMINI_API_KEY

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(8192), b""):
            h.update(b)
    return h.hexdigest()

def load_config(config_path):
    cfg = {
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "chunk_size": 500,
        "overlap": 50,
        "retrieval_top_k": 5,
        "llm_model": "gemini-1.5-flash",
        "prompt_template": "You are an AI document assistant. Use the extracted document context to answer clearly and accurately.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    }
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            j = json.load(f)
        cfg["embedding_model"] = j.get("embedding", {}).get("model", cfg["embedding_model"])
        cfg["chunk_size"] = j.get("embedding", {}).get("chunk_size", cfg["chunk_size"])
        cfg["overlap"] = j.get("embedding", {}).get("overlap", cfg["overlap"])
        cfg["retrieval_top_k"] = j.get("rag", {}).get("retrieval_top_k", cfg["retrieval_top_k"])
        cfg["llm_model"] = j.get("rag", {}).get("llm", cfg["llm_model"])
        cfg["prompt_template"] = j.get("rag", {}).get("prompt_template", cfg["prompt_template"])
    return cfg

def chunk_text(s, size=500, overlap=50):
    s = s or ""
    if not s: return []
    out, i, step = [], 0, max(1, size - overlap)
    while i < len(s):
        out.append(s[i:i+size])
        i += step
    return out

def build_or_load_index(extracted_json, cache_dir, embedding_model, size, overlap):
    os.makedirs(cache_dir, exist_ok=True)
    with open(extracted_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    base_text = " ".join(data.get("texts", []))
    tables = [json.dumps(t, ensure_ascii=False) for t in data.get("tables", [])]
    pics = [p.get("caption", "") for p in data.get("pictures", [])]
    chunks = chunk_text(base_text, size=size, overlap=overlap) + tables + pics

    key = sha256(extracted_json) + f":{size}:{overlap}:{embedding_model}"
    hash_file = os.path.join(cache_dir, "data_hash.txt")
    idx_file = os.path.join(cache_dir, "faiss_index.bin")
    emb_file = os.path.join(cache_dir, "embeddings.npy")
    chunks_file = os.path.join(cache_dir, "chunks.json")

    rebuild = True
    if all(os.path.exists(p) for p in [hash_file, idx_file, emb_file, chunks_file]):
        if open(hash_file).read().strip() == key:
            rebuild = False

    embedder = SentenceTransformer(embedding_model)
    if rebuild:
        embs = embedder.encode(chunks, show_progress_bar=False)
        dim = embs.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embs).astype("float32"))
        faiss.write_index(index, idx_file)
        np.save(emb_file, embs)
        with open(chunks_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        with open(hash_file, "w") as f:
            f.write(key)
    else:
        index = faiss.read_index(idx_file)
        np.load(emb_file)
        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    return embedder, index, chunks

def retrieve_with_scores(query, index, chunks, embedder, k=5):
    qv = embedder.encode([query])
    dists, idxs = index.search(np.array(qv).astype("float32"), k)
    return [(chunks[i], float(dists[0][j])) for j, i in enumerate(idxs[0])]

def answer_question(query, use_rag, index, chunks, embedder, model_id, prompt_template, k=5):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_id)
    if use_rag and index is not None and chunks:
        top = retrieve_with_scores(query, index, chunks, embedder, k=k)
        context = "\n".join([c for c, _ in top])
        prompt = (prompt_template or "Use the following document context to answer.\n\nContext:\n{context}\n\nQuestion: {question}").format(
            context=context, question=query
        )
    else:
        prompt = f"Answer the question without document context:\n{query}"
    resp = model.generate_content(prompt, generation_config={"temperature": 0.2})
    return resp.text.strip()