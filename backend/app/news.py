from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .deps import get_current_user
from .models import NewsItem
from .schemas import NewsItemCreate
from .ai_agent import verify_claim

router = APIRouter()

VERIFICATION_THRESHOLD = 60  # minimum score to accept news


@router.get("/feed")
def get_feed(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    For now: return all verified news items from DB.
    If DB is empty, you can pre-populate manually later or insert via /news/upload.
    """
    items = db.query(NewsItem).filter(NewsItem.status == "verified").order_by(NewsItem.created_at.desc()).all()
    # Convert to simple dicts (we're not using Pydantic response model here to keep it quick)
    return [
        {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "status": item.status,
            "genuineness_score": item.genuineness_score,
            "verdict_summary": item.verdict_summary,
            "created_at": item.created_at.isoformat(),
        }
        for item in items
    ]


@router.post("/upload")
async def upload_news(
    news: NewsItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Creator upload endpoint:
    - Takes title + description (news text).
    - Runs AI verification.
    - If score >= threshold -> save as verified news.
    - Else -> return feedback and do NOT save.
    """
    text_to_verify = f"{news.title}\n\n{news.description}"

    try:
        result = await verify_claim(text_to_verify)
    except Exception as e:
        # If AI fails, reject but explain
        raise HTTPException(
            status_code=500,
            detail=f"Verification service error: {str(e)}",
        )

    verdict = result.get("verdict", "Uncertain")
    score = int(result.get("score", 0))
    bullets = result.get("bullets", [])

    if score >= VERIFICATION_THRESHOLD and verdict in ["True", "Mixed"]:
        # Accept and save news
        new_item = NewsItem(
            title=news.title,
            description=news.description,
            status="verified",
            genuineness_score=score,
            verdict_summary="\n".join(bullets),
            creator_id=current_user.id,
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return {
            "status": "approved",
            "news_id": new_item.id,
            "verdict": verdict,
            "score": score,
            "bullets": bullets,
        }
    else:
        # Reject but provide feedback, do not save
        return {
            "status": "rejected",
            "verdict": verdict,
            "score": score,
            "bullets": bullets,
        }
