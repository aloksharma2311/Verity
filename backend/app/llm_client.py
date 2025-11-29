# backend/app/llm_client.py

import os
import json
from typing import Dict, Any

import httpx
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.groq.com/openai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")


def analyze_with_llm(prompt: str) -> Dict[str, Any]:
    """
    Call Groq's OpenAI-compatible chat API in a synchronous way.
    Always returns a dict with keys: verdict, score, bullets.
    """
    if not LLM_API_KEY:
        return {
            "verdict": "Uncertain",
            "score": 50,
            "bullets": ["LLM_API_KEY not set; running in fallback mode."],
        }

    url = f"{LLM_API_BASE.rstrip('/')}/chat/completions"

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a rigorous news verification agent. "
                    "You MUST respond ONLY with a valid JSON object with keys: "
                    "verdict (one of: True, False, Mixed, Uncertain), "
                    "score (0-100 integer), and bullets (list of short strings)."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
    }

    try:
        with httpx.Client(timeout=20) as client:
            resp = client.post(url, headers=headers, json=body)
    except Exception as e:
        return {
            "verdict": "Uncertain",
            "score": 40,
            "bullets": [f"LLM request failed: {e}"],
        }

    if resp.status_code != 200:
        text = ""
        try:
            text = resp.text
        except Exception:
            text = f"HTTP {resp.status_code}"
        return {
            "verdict": "Uncertain",
            "score": 45,
            "bullets": [
                "Groq API returned an error.",
                f"Status: {resp.status_code}",
                f"Details: {text[:200]}",
            ],
        }

    data = resp.json()
    content = data["choices"][0]["message"]["content"].strip()

    # Try to parse JSON from the model content
    try:
        parsed = json.loads(content)
        verdict = str(parsed.get("verdict", "Uncertain"))
        score = int(parsed.get("score", 50))
        bullets = parsed.get("bullets", [])
        if not isinstance(bullets, list):
            bullets = [str(bullets)]
    except Exception:
        # Model didn't strictly follow JSON; still return something
        verdict = "Uncertain"
        score = 50
        bullets = [content]

    return {
        "verdict": verdict,
        "score": score,
        "bullets": bullets,
    }
