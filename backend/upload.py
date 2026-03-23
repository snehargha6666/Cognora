from fastapi import APIRouter, UploadFile, File
from file_parser import extract_text
from chunking import chunk_text
from embeddings import get_embedding
from fetcher import fetch_research_papers

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1. Extract text
    text = await extract_text(file)

    # 2. Chunk
    chunks = chunk_text(text)

    # 3. Embed (optional for now)
    embeddings = [get_embedding(c) for c in chunks[:5]]

    # 4. Build query (IMPORTANT)
    query = " ".join(chunks[:3])[:1000]

    # 5. Fetch research papers
    papers = fetch_research_papers(query)

    return {
        "filename": file.filename,
        "papers": papers
    }