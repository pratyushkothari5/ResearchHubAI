
# Placeholder for vector database utilities

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> list:
    """Convert text to vector embedding."""
    return model.encode(text).tolist()


def cosine_similarity(vec1: list, vec2: list) -> float:
    """Compute cosine similarity between two vectors."""
    a, b = np.array(vec1), np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def find_relevant_papers(query: str, papers: list, top_k: int = 3) -> list:
    """
    Given a query and a list of paper dicts (with 'abstract' field),
    return the top_k most relevant papers by cosine similarity.
    """
    if not papers:
        return []
    query_vec = embed_text(query)
    scored = []
    for paper in papers:
        abstract = paper.abstract or ""
        paper_vec = embed_text(abstract)
        score = cosine_similarity(query_vec, paper_vec)
        scored.append((score, paper))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:top_k]]
