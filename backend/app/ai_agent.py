# backend/app/ai_agent.py

from typing import Dict, Any, List

from .llm_client import analyze_with_llm
from .gnews_client import fetch_related_news


def _build_prompt_for_claim(claim_text: str, articles: List[Dict[str, Any]]) -> str:
    """
    Build the LLM prompt: includes the claim and a compact list of retrieved news articles.
    """
    lines = []
    lines.append("You are a news verification AI agent.")
    lines.append("Task: Decide if the given claim is True, False, Mixed, or Uncertain.")
    lines.append("")
    lines.append("Claim to check:")
    lines.append(claim_text.strip())
    lines.append("")
    lines.append("Related news articles (from GNews):")

    if not articles:
        lines.append("- (No related news articles found.)")
    else:
        for idx, art in enumerate(articles[:5], start=1):
            lines.append(
                f"- [{idx}] {art.get('title','')} "
                f"(source={art.get('source','')}, published_at={art.get('published_at','')})"
            )

    lines.append("")
    lines.append(
        "Use ONLY this information and your general world knowledge up to now. "
        "Output STRICTLY a JSON object with keys: verdict (True/False/Mixed/Uncertain), "
        "score (0-100 integer, higher=more confident), and bullets (array of short explanation strings)."
    )

    return "\n".join(lines)


def verify_text_claim(text: str) -> Dict[str, Any]:
    """
    Main function used by the chatbot: verifies a text claim/headline.
    Returns dict: { verdict, score, bullets, articles }
    """
    claim = text.strip()
    if not claim:
        return {
            "verdict": "Uncertain",
            "score": 0,
            "bullets": ["Empty claim provided."],
            "articles": [],
        }

    # 1) Fetch related news
    articles = fetch_related_news(claim)

    # 2) Build prompt for LLM
    prompt = _build_prompt_for_claim(claim, articles)

    # 3) Call LLM
    llm_result = analyze_with_llm(prompt)

    verdict = str(llm_result.get("verdict", "Uncertain"))
    try:
        score = int(llm_result.get("score", 50))
    except Exception:
        score = 50
    bullets = llm_result.get("bullets", [])
    if not isinstance(bullets, list):
        bullets = [str(bullets)]

    return {
        "verdict": verdict,
        "score": score,
        "bullets": bullets,
        "articles": articles,
    }


def verify_claim(text: str) -> Dict[str, Any]:
    """
    Compatibility wrapper for /news/upload if it imports verify_claim().
    """
    return verify_text_claim(text)
