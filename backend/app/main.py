from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.auth import router as auth_router
from app.news import router as news_router
from app.chat import router as chat_router
from app.database import Base, engine
from dotenv import load_dotenv
load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Verity Hackathon API", version="0.1.0")

# ----------------------
# SECURITY SCHEME FIX
# ----------------------
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT"
)

@app.get("/health")
def health():
    return {"status": "OK"}

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(news_router, prefix="/news", tags=["news"])
app.include_router(chat_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
