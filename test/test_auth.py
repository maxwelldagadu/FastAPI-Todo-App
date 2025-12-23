from fastapi import status,HTTPException
import pytest
from jose import jwt,JWTError
from routers.auth import login_token,get_user
from dotenv import load_dotenv
import os


load_dotenv()

# test authentication

@pytest.mark.asyncio
async def test_authentication(post_user_conn,create_user):
    auth_payload =  {"username":"maxwell@gmail.com","password":"qwerty"}

    auth_response = await post_user_conn.post("/auth/login",data=auth_payload)
    assert auth_response.status_code == status.HTTP_200_OK

# test wrong crednetials

@pytest.mark.asyncio
async def test_wrong_credentials(post_user_conn,create_user):
    wrong_payload = {"username":"maxwell@gmail.com","password":"qwert"}

    wrong_response = await post_user_conn.post("auth/login",data=wrong_payload)
    assert wrong_response.status_code == status.HTTP_401_UNAUTHORIZED


# test token creation

def test_token_creation():
    email = "maxwell@gmail.com"
    id = 1

    user = login_token(email,id)

    decode_token = jwt.decode(user,os.getenv("SECRET_KEY"),algorithms=[os.getenv("ALGORITHM")])
    
    assert decode_token["sub"] == email
    assert decode_token["id"] == id


# test get current user

@pytest.mark.asyncio
async def test_get_current_user():
    token = {"sub":"maxwell@gmail.com","id":1}
    encode = jwt.encode(token,os.getenv("SECRET_KEY"),os.getenv("ALGORITHM"))
    
    decode = await get_user(encode)

    assert decode["id"] == 1

# test current user is valid

@pytest.mark.asyncio
async def test_invalid_current_user():
    user_info = {"sub":"maxwell@gmail.com","id":None}
    user_encode = jwt.encode(user_info,os.getenv("SECRET_KEY"),os.getenv("ALGORITHM"))
    
    with pytest.raises(HTTPException) as pytestexception:
        user_decode = await get_user(user_encode)
        
        assert pytestexception.value.status_code == status.HTTP_401_UNAUTHORIZED 
        assert pytestexception.value.detail == " Invalid User Credentials"


        