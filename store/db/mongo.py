from motor.motor_asyncio import AsyncioMotorClient
from store.core.config import settings

class MongoClient:
    def __init__(self) -> None:
        self.client: AsyncioMotorClient = AsyncioMotorClient(settings.DATABASE_URL)
    
    def get(self) -> AsyncioMotorClient:
        return self.client


db_client = MongoClient()