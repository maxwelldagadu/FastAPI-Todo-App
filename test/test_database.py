
from  app.models import Base
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.pool import StaticPool




TEST_DB = "sqlite+aiosqlite:///./test_db.sqlite3"

engine = create_async_engine(TEST_DB,connect_args={"check_same_thread":False},poolclass=StaticPool)

async_session = async_sessionmaker(bind=engine,autocommit=False,autoflush=False,class_=AsyncSession,expire_on_commit=True)

# test create database tables
async def override_create_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# test get database session
async def override_get_db():
    async with async_session() as session:
        yield session

# create test function for current user
def override_current_user():
    return {"id": 1}
    



