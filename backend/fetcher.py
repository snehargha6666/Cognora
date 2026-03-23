import requests
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"

def fetch_arxiv(query: str, max_results=20):
    url = f"{ARXIV_API}?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)

    root = ET.fromstring(response.content)

    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
        link = entry.find("{http://www.w3.org/2005/Atom}id").text.strip()

        papers.append({
            "title": title,
            "summary": summary,
            "link": link
        })

    return papers