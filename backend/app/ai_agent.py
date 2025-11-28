from typing import Dict, Any

from .gnews_client import search_news
from .llm_client import analyze_with_llm


async def verify_claim(text: str) -> Dict[str, Any]:
    """
    Main verification pipeline:
    1. Search related articles via GNews.
    2. Build a context summary.
    3. Ask LLM (Groq) for verdict, score, and bullets.
    """

    # 1) Get news from GNews
    try:
        news_json = await search_news(text)
        articles = news_json.get("articles", [])
    except Exception as e:
        # If GNews fails, still let LLM handle it
        articles = []
        gnews_error = str(e)
    else:
        gnews_error = None

    # 2) Build article summary for the LLM
    if articles:
        article_summaries = "\n".join(
            f"- {a.get('title')} ({a.get('source', {}).get('name')}): "
            f"{a.get('description')}"
            for a in articles
        )
    else:
        article_summaries = "No related articles were found via GNews."

    # 3) Build prompt for LLM
    prompt = f"""
Claim:
{text}

Related news context from GNews:
{article_summaries}

Task:
Based on the claim and the news context:
1. Decide if the claim is True, False, Mixed, or Uncertain.
2. Give a confidence score between 0 and 100.
3. Provide 2–4 short bullet-point explanations.

Return ONLY a JSON object with this structure:
{{
  "verdict": "True | False | Mixed | Uncertain",
  "score": 0-100,
  "bullets": ["...", "..."]
}}
"""

    # 4) Ask LLM
    llm_result = await analyze_with_llm(prompt)

    # Attach some debug info (optional)
    llm_result["article_count"] = len(articles)
    if gnews_error:
        llm_result["gnews_error"] = gnews_error

    return llm_result
