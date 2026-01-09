import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url: str):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except:
        raise Exception("Failed to fetch Wikipedia page")

    soup = BeautifulSoup(res.text, "html.parser")

    # ---------------- Title ----------------
    title = soup.find("h1").text.strip()

    # ---------------- Summary ----------------
    summary = ""
    for p in soup.select("p"):
        if p.text.strip():
            summary = p.text.strip()
            break

    # ---------------- Sections ----------------
    sections = []
    for h in soup.select("h2 span.mw-headline"):
        sections.append(h.text.strip())

    # ---------------- Main content ----------------
    paragraphs = soup.select("p")
    content = "\n".join([p.text for p in paragraphs])

    return {
        "title": title,
        "summary": summary,
        "sections": sections[:10],
        "content": content
    }
