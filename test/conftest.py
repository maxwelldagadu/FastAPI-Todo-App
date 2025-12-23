import pytest_asyncio
from main import app
from httpx import AsyncClient,ASGITransport
from app.database import db_dependency
from .test_database import override_get_db,override_current_user,engine,async_session
from app.database import Base
from routers.auth import get_user
from.test_database import override_create_test_db
from app.models import  Todos,User
from routers.passhashing import Hash


# create fixture for AsyncClient
@pytest_asyncio.fixture(loop_scope="function")
async def set_http_conn():

    """ Run Dependency Overides for db_injection, cc_user and token_bearer functions """

    app.dependency_overrides[db_dependency] = override_get_db
    app.dependency_overrides[get_user] = override_current_user
    
    # create all tables
    await override_create_test_db()

    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as client:
        yield client

    
    app.dependency_overrides.clear()    # close the overrides

    # delete all data from database after successful test

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# create mock for the Todo table

@pytest_asyncio.fixture(loop_scope="function")
async def todo_create():
        todo = Todos(id=1,title="Testing",description="Application Testing",priority=5,complete=False,user_id=1)
        db = async_session()
        db.add(todo)
        await db.commit()

# create user fixture

@pytest_asyncio.fixture(loop_scope="function")
async def create_user():
    user = User(first_name="RRR",last_name="Yoo",email="maxwell@gmail.com",hashed_password=Hash.hash_passwd("qwerty"),phone="+233547786079")
    db = async_session()
    db.add(user)
    await db.commit()

# fixturw for ceate a user

@pytest_asyncio.fixture(loop_scope="function")
async def post_user_conn():
    
    # dependency overrride
    app.dependency_overrides[db_dependency] = override_get_db

    # create table
    await override_create_test_db()


    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as client:
        yield client
    

    # clear override
    app.dependency_overrides.clear()
    
    # drop table
    async with  engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



