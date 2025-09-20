from langchain.vectorstores import FAISS
from llm_setup import embeddings

def create_db():
    return FAISS.from_texts([], embeddings)

def add_entry(db, text):
    db.add_texts([text])

def search_entries(db, query, k=3):
    return db.similarity_search(query, k=k)