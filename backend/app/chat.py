from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .deps import get_current_user
from .ai_agent import verify_claim

from typing import Dict, Any

router = APIRouter()


class ChatVerifyRequest:
    claim: str


@router.post("/verify")
async def chat_verify(payload: Dict[str, Any],
                      db: Session = Depends(get_db),
                      current_user=Depends(get_current_user)):
    """
    Chatbot endpoint: user sends a text claim, we verify it.
    Body: { "claim": "some news text" }
    """
    claim = payload.get("claim")
    if not claim:
        raise HTTPException(status_code=400, detail="Missing 'claim' in request body")

    try:
        result = await verify_claim(claim)
    except Exception as e:
        # In case GNews/LLM fails (no internet, bad key, etc.), don't crash the app.
        return {
            "verdict": "Uncertain",
            "score": 0,
            "bullets": [
                "Verification service is temporarily unavailable.",
                f"Internal error: {str(e)}",
            ],
            "article_count": 0,
        }

    return result
