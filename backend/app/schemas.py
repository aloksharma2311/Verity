from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------- User ----------

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2, use orm_mode=True if v1


# ---------- Auth ----------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- News ----------

class NewsItemBase(BaseModel):
    title: str
    description: str


class NewsItemCreate(NewsItemBase):
    pass


class NewsItemOut(NewsItemBase):
    id: int
    status: str
    genuineness_score: Optional[int] = None
    verdict_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
