import numpy as np, faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

def hierarchical_summarize(corpus, model_id="gemini-1.5-flash", api_key=None, size=2000, overlap=300):
    if api_key: genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_id)
    def _chunk(s, sz, ov):
        out,i,step=[],0,max(1,sz-ov)
        while i<len(s): out.append(s[i:i+sz]); i+=step
        return out
    big = "\n".join(corpus)
    lvl1=[]
    for ch in _chunk(big, size, overlap):
        lvl1.append(model.generate_content("Summarize focusing on key facts:\n\n"+ch).text.strip())
    lvl2 = model.generate_content("Create a concise hierarchical summary of the following:\n\n"+ "\n\n".join(lvl1)).text.strip()
    return lvl1, lvl2

def qa_over_corpus(corpus, questions, embedding_model="all-MiniLM-L6-v2", model_id="gemini-1.5-flash", api_key=None, k=5):
    if api_key: genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_id)
    embedder = SentenceTransformer(embedding_model)
    embs = embedder.encode(corpus, show_progress_bar=False)
    dim = embs.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embs).astype("float32"))
    out=[]
    for q in questions:
        qv = embedder.encode([q])
        d, ix = index.search(np.array(qv).astype("float32"), k)
        top = [(corpus[i], float(d[0][j])) for j,i in enumerate(ix[0])]
        ctx = "\n".join([t for t,_ in top])
        ans = model.generate_content(f"Use the context to answer clearly.\n\nContext:\n{ctx}\n\nQuestion: {q}\n\nAnswer:", generation_config={"temperature":0.2}).text.strip()
        out.append({"question": q, "answer": ans, "top_contexts": [{"text": t, "dist": s} for t,s in top]})
    return out