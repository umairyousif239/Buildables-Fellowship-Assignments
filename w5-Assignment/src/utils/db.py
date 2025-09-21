# src/utils/db.py

import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema import Document
from typing import List, Tuple, Union

# -----------------------------
# Create and return an empty FAISS vector DB sized to embedding dimension.
# -----------------------------
def create_db(embeddings=None) -> FAISS:
    """
    Create an empty FAISS DB with the correct embedding dimensions.
    Returns a FAISS wrapper object.
    
    If embeddings is not provided, raises a ValueError.
    """
    if embeddings is None:
        raise ValueError(
            "Embeddings not initialized. Please provide a valid HuggingFace embeddings instance."
        )
    # -----------------------------
    # Get the dimension size from a dummy embedding
    # -----------------------------
    dummy_vector = embeddings.embed_query("init")
    dimension = len(dummy_vector)

    # -----------------------------
    # Create empty FAISS index
    # -----------------------------
    index = faiss.IndexFlatL2(dimension)

    # -----------------------------
    # Initialize FAISS wrapper with proper docstore
    # -----------------------------
    return FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore({}),
        index_to_docstore_id={}
    )

# -----------------------------
# Add one or more texts as Documents into the FAISS DB.
# -----------------------------
def add_entry(db: FAISS, texts: Union[str, List[str]]):
    """
    Add one or more documents into the FAISS DB.
    Converts texts into Document objects.
    """
    if not texts:
        return

    # -----------------------------
    # Accept a single string or a list of strings
    # -----------------------------
    if isinstance(texts, str):
        texts = [texts]

    docs = [Document(page_content=text) for text in texts]
    db.add_documents(docs)

# -----------------------------
# Semantic search in FAISS; return top-k (Document, score) tuples.
# -----------------------------
def search(db: FAISS, query: str, k: int = 3) -> List[Tuple[Document, float]]:
    """
    Perform semantic search in FAISS DB.
    Returns top-k documents with similarity scores as tuples: (Document, score)
    """
    if not query:
        return []

    results = db.similarity_search_with_score(query, k=k)
    return results
