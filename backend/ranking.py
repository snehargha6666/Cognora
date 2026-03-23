import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from backend.embeddings import get_embedding

def semantic_rank(query, papers, top_k=5):
    if not papers:
        return []

    query_vec = get_embedding(query).reshape(1, -1)
    paper_vecs = np.array([get_embedding(p["summary"]) for p in papers])

    similarities = cosine_similarity(query_vec, paper_vecs)[0]
    ranked_indices = np.argsort(similarities)[::-1][:top_k]

    return [papers[i] for i in ranked_indices]