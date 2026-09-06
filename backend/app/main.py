import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import data, conversation, chat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="빈집 인사이트 AI 비서 API",
    version="1.0.0",
    description="전국 빈집 13만 4천 호 시계열 데이터 기반 컨텍스트 주입 AI 비서 API"
)

# CORS 설정
allowed = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)
app.include_router(conversation.router)
app.include_router(chat.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Vacant House AI Service is Running"}