# utils.py
import requests
from bs4 import BeautifulSoup
import json
from pypdf import PdfReader

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def clean_text(text: str) -> str:
    text = " ".join(text.split())
    return text.strip()

def extract_text_from_url(url: str, max_elements: int = 40) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        texts = []

        for tag in soup.find_all(["p", "h1", "h2", "h3"])[:max_elements]:
            texts.append(tag.get_text(strip=True))

        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            texts.append(meta["content"])

        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    texts.extend([str(v) for v in data.values() if isinstance(v, str)])
            except Exception:
                continue

        combined = clean_text(" ".join(texts))
        return combined if combined else "[No meaningful public text found]"

    except Exception as e:
        return f"[Error fetching content from {url}: {e}]"

def extract_text_from_pdf(file, max_pages: int = 10) -> str:
    try:
        reader = PdfReader(file)
        pages = []
        for page in reader.pages[:max_pages]:
            if page.extract_text():
                pages.append(page.extract_text())
        return clean_text(" ".join(pages))
    except Exception:
        return ""



