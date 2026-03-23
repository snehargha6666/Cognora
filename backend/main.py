from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from serpapi.google_search import GoogleSearch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

# CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

SERP_API_KEY = "78ca343f96ba067c64ef3f9196db5fc3f943bb49d94509c30e0f20b47a01e22f"

class Query(BaseModel):
    query: str


@app.post("/search")
def semantic_search(q: Query):
    # 🔍 Step 1: Get Google results
    params = {
        "q": q.query,
        "api_key": SERP_API_KEY,
        "engine": "google_scholar"
    }

    search = GoogleSearch(params)
    data = search.get_dict()

    organic = data.get("organic_results", [])

    # Extract titles + snippets
    texts = []
    results = []

    for item in organic[:10]:
        text = item.get("title", "") + " " + item.get("snippet", "")
        texts.append(text)

        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "url": item.get("link")
        })

    if not texts:
        return {"results": []}

    # 🧠 Step 2: Semantic embeddings
    query_embedding = model.encode([q.query])
    doc_embeddings = model.encode(texts)

    # 📊 Step 3: Similarity scoring
    scores = cosine_similarity(query_embedding, doc_embeddings)[0]

    # 🔥 Step 4: Re-rank
    ranked = sorted(
        zip(scores, results),
        key=lambda x: x[0],
        reverse=True
    )

    final_results = [item[1] for item in ranked[:5]]

    return {"results": final_results}