from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    engine, 
    class_ = AsyncSession, 
    expire_on_commit = False
)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session