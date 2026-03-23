import requests
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"


# 🔹 Fetch from arXiv
def fetch_arxiv(query: str, max_results=10):
    url = f"{ARXIV_API}?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)

    root = ET.fromstring(response.content)

    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()

        summary_elem = entry.find("{http://www.w3.org/2005/Atom}summary")
        summary = summary_elem.text.strip() if summary_elem is not None else ""

        link = entry.find("{http://www.w3.org/2005/Atom}id").text.strip()

        papers.append({
            "title": title,
            "abstract": summary,   # normalized key
            "url": link,
            "source": "arxiv"
        })

    return papers


# 🔹 Fetch from Semantic Scholar (STRONGER)
def fetch_semantic_scholar(query: str, max_results=10):
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,abstract,authors,year,url"
    }

    response = requests.get(SEMANTIC_SCHOLAR_API, params=params)
    data = response.json()

    papers = []

    for p in data.get("data", []):
        papers.append({
            "title": p.get("title"),
            "abstract": p.get("abstract") or "",
            "url": p.get("url"),
            "authors": [a["name"] for a in p.get("authors", [])],
            "year": p.get("year"),
            "source": "semantic_scholar"
        })

    return papers


# 🔥 COMBINED FETCH (THIS IS WHAT YOU USE)
def fetch_research_papers(query: str, max_results=10):
    arxiv_papers = fetch_arxiv(query, max_results // 2)
    semantic_papers = fetch_semantic_scholar(query, max_results // 2)

    combined = arxiv_papers + semantic_papers

    return combined