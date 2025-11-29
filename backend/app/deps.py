# app/auth.py  (or wherever this lives)

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from .database import get_db
from .models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallbacksecret")
ALGORITHM = "HS256"

# 👇 IMPORTANT: auto_error=False so missing/invalid token does NOT auto-401
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


class DemoUser:
    """Very lightweight demo user used when no valid token is provided."""
    id = 0
    email = "demo@verity.app"
    name = "Verity Demo User"


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    - If a valid JWT is present → return real User from DB.
    - If no token / bad token → return DemoUser (no 401, good for demo).
    """

    # 🔹 No token at all → anonymous / demo mode
    if not token:
        return DemoUser()

    # 🔹 Try normal JWT auth
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            # bad token → fall back to demo user instead of 401
            return DemoUser()
    except JWTError:
        # bad token → fall back to demo user instead of 401
        return DemoUser()

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        # no such user → also fall back to demo
        return DemoUser()

    return user
