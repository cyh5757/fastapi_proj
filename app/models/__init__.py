from app.config import MONGO_URL, MONGO_DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine


class MongoDB:

    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(client=self.client, database=MONGO_DB_NAME)
        print("MongoDB 연결 성공")

    def close(self):
        self.client.close()
        print("MongoDB 연결 종료")


mongodb = MongoDB()
