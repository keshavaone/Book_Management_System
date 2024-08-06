# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
from .models import Base

engine = create_async_engine(
    DATABASE_URL, echo=True
)

async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

async def init_db():
    async with engine.begin() as conn:
        # Run any initialization commands, such as creating tables
        await conn.run_sync(Base.metadata.create_all)
