from fastapi import APIRouter
from pydantic import BaseModel

from backend.fetcher import fetch_arxiv
from backend.ranking import semantic_rank
from backend.summarizer import summarize_text

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search")
def search(req: SearchRequest):
    papers = fetch_arxiv(req.query)
    ranked = semantic_rank(req.query, papers, req.top_k)

    for paper in ranked:
        paper["short_summary"] = summarize_text(paper["summary"])

    return {"results": ranked}