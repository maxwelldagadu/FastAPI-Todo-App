from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from .models import Base
from fastapi import Depends
from typing import Annotated

load_dotenv()

# database engine

engine = create_async_engine(os.getenv("DATABASE_URL"),echo=False)

# database session maker

async_session_maker = async_sessionmaker(bind=engine,autoflush=False,autocommit=False,class_=AsyncSession,
                                                                                   expire_on_commit=False)


# creating our database tables

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# database dependency

async def db_dependency():
    async with async_session_maker() as session:
        yield session

db_injection = Annotated[AsyncSession, Depends(db_dependency)]