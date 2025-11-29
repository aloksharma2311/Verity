# backend/app/gnews_client.py

import os
from typing import List, Dict, Any

import httpx
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
GNEWS_BASE_URL = "https://gnews.io/api/v4/search"


def fetch_related_news(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Simple wrapper around GNews /search endpoint.
    Returns a list of normalized article dicts.
    If key missing or network fails, returns [].
    """
    if not GNEWS_API_KEY:
        return []

    params = {
        "q": query,
        "lang": "en",
        "country": "in",  # you can tweak later
        "max": max_results,
        "apikey": GNEWS_API_KEY,
    }

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(GNEWS_BASE_URL, params=params)
    except Exception:
        return []

    if resp.status_code != 200:
        return []

    data = resp.json()
    articles = data.get("articles", []) or []

    normalized = []
    for a in articles:
        normalized.append(
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", ""),
                "source": (a.get("source") or {}).get("name", ""),
                "published_at": a.get("publishedAt", ""),
            }
        )

    return normalized
