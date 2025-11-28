import os
import httpx

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

if not GNEWS_API_KEY:
    raise RuntimeError("GNEWS_API_KEY is not set in .env")


async def search_news(query: str) -> dict:
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "lang": "en",
        "max": 5,
        "apikey": GNEWS_API_KEY,  # important: 'apikey'
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)

    resp.raise_for_status()
    return resp.json()
