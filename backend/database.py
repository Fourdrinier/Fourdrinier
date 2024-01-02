import os
import secrets
from typing import cast, Type

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
    f"@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
)
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=cast(Type[AsyncSession], AsyncSession), expire_on_commit=False
)


def generate_unique_id():
    return secrets.token_urlsafe(8)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            # Handle or log the exception as needed
            raise
