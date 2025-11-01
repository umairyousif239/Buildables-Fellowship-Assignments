import os, json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def _chunk(s, size, overlap):
    out, i, step = [], 0, max(1, size - overlap)
    while i < len(s):
        out.append(s[i:i+size]); i += step
    return out

def _build_index(chunks, embedder):
    embs = embedder.encode(chunks, show_progress_bar=False)
    dim = embs.shape[1]; idx = faiss.IndexFlatL2(dim)
    idx.add(np.array(embs).astype("float32"))
    return idx

def _retrieve(idx, chunks, embedder, q, k=5):
    qv = embedder.encode([q])
    d,i = idx.search(np.array(qv).astype("float32"), k)
    return [(chunks[ii], float(d[0][j])) for j, ii in enumerate(i[0])]

def run_chunking_experiments(extracted_json, configs, questions, embedding_model="all-MiniLM-L6-v2"):
    with open(extracted_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    base = " ".join(data.get("texts", []))
    tables = [json.dumps(t, ensure_ascii=False) for t in data.get("tables", [])]
    pics = [p.get("caption", "") for p in data.get("pictures", [])]
    embedder = SentenceTransformer(embedding_model)

    lines = []
    for cfg in configs:
        chunks = _chunk(base, cfg["size"], cfg["overlap"]) + tables + pics
        idx = _build_index(chunks, embedder)
        lines.append(f"## size={cfg['size']} overlap={cfg['overlap']} total_chunks={len(chunks)}")
        for q in questions:
            top = _retrieve(idx, chunks, embedder, q, k=5)
            lines.append(f"- Q: {q}")
            for i,(ch,d) in enumerate(top,1):
                snippet = ch.replace("\n"," ")[:160]
                lines.append(f"  - {i}) dist={d:.2f} • {snippet}{'...' if len(ch)>160 else ''}")
        lines.append("")
    return "\n".join(["# Chunking Experiments", ""] + lines)