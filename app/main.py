from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from pathlib import Path
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import MONGO_URL, MONGO_DB_NAME

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # MongoDB 연결 설정

    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[MONGO_DB_NAME]
    print("MongoDB 연결 성공")
    yield
    # 종료 시 실행
    # 여기에 on_app_shutdown 함수의 내용을 넣습니다
    print("MongoDB 연결 종료")
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=BASE_DIR / "templates")
