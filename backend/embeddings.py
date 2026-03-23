from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once (IMPORTANT)
model = SentenceTransformer("all-MiniLM-L6-v2")


# 🔹 Single embedding
def get_embedding(text: str):
    return model.encode(text, normalize_embeddings=True)


# 🔹 Batch embeddings (FASTER for chunks)
def get_embeddings(texts: list[str]):
    return model.encode(texts, normalize_embeddings=True)


# 🔹 Cosine similarity
def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2))


# 🔹 Rank chunks by relevance to query
def rank_by_similarity(query: str, chunks: list[str]):
    query_emb = get_embedding(query)
    chunk_embs = get_embeddings(chunks)

    scores = []
    for i, emb in enumerate(chunk_embs):
        score = cosine_similarity(query_emb, emb)
        scores.append((chunks[i], score))

    # Sort highest similarity first
    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


# 🔹 Extract best chunks (for building research query)
def get_top_chunks(query: str, chunks: list[str], top_k: int = 3):
    ranked = rank_by_similarity(query, chunks)
    return [chunk for chunk, _ in ranked[:top_k]]