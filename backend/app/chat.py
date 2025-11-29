# backend/app/chat.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db
from .ai_agent import verify_text_claim

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


class ChatVerifyRequest(BaseModel):
    text: str


class ChatVerifyResponse(BaseModel):
    verdict: str
    score: int
    bullets: list[str]


@router.post("/verify", response_model=ChatVerifyResponse)
def chat_verify(
    payload: ChatVerifyRequest,
    db: Session = Depends(get_db),  # reserved for logging later
):
    """
    Chatbot endpoint: verify a news claim / headline from plain text.
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        result = verify_text_claim(payload.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Verification failed: {e}",
        )

    return ChatVerifyResponse(
        verdict=str(result.get("verdict", "Uncertain")),
        score=int(result.get("score", 50)),
        bullets=list(result.get("bullets", [])),
    )
