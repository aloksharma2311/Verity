# backend/app/llm_client.py

import os
import json
import httpx
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.groq.com/openai/v1")

# ✅ FIX: use a current Llama 3.1 model instead of decommissioned ones
LLM_MODEL = "llama-3.1-8b-instant"


async def analyze_with_llm(prompt: str) -> Dict:
    """
    Call Groq's OpenAI-compatible chat API.
    If anything goes wrong (400/401/etc.), return a safe fallback
    instead of crashing the backend.
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
                    "You MUST respond ONLY with a valid JSON object."
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
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(url, headers=headers, json=body)
    except Exception as e:
        return {
            "verdict": "Uncertain",
            "score": 40,
            "bullets": [f"LLM request failed: {e}"],
        }

    if resp.status_code != 200:
        try:
            err_text = resp.text
        except Exception:
            err_text = f"HTTP {resp.status_code}"
        return {
            "verdict": "Uncertain",
            "score": 45,
            "bullets": [
                "Groq API returned an error.",
                f"Status: {resp.status_code}",
                f"Details: {err_text[:200]}",
            ],
        }

    data = resp.json()
    content = data["choices"][0]["message"]["content"].strip()

    try:
        parsed = json.loads(content)
        verdict = str(parsed.get("verdict", "Uncertain"))
        score = int(parsed.get("score", 50))
        bullets = parsed.get("bullets", [])
        if not isinstance(bullets, list):
            bullets = [str(bullets)]
    except Exception:
        verdict = "Uncertain"
        score = 50
        bullets = [content]

    return {
        "verdict": verdict,
        "score": score,
        "bullets": bullets,
    }
