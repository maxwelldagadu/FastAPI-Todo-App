from fastapi import status
import pytest
from routers.passhashing import Hash




# create a user

@pytest.mark.asyncio
async def test_create_user(post_user_conn):
    post_payload = {"first_name":"Maxi",
                    "last_name":"Dagadu",
                    "email":"max@gmail.com",
                    "password":Hash.hash_passwd("qwerty"),
                    "phone":"tel:+233-54-778-6079"}
    
    create_response= await post_user_conn.post("/user/create",json=post_payload)
    assert create_response.status_code == status.HTTP_200_OK
    assert create_response.json() == {"first_name":"Maxi",
                                      "last_name":"Dagadu",
                                      "email":"max@gmail.com",
                                      "is_active":1,
                                      "phone":"tel:+233-54-778-6079"}
    
# get a user

@pytest.mark.asyncio
async def test_get_me(set_http_conn,create_user):
    me_response = await set_http_conn.get("/user/me")
    assert me_response.status_code == status.HTTP_200_OK
   
# change password

@pytest.mark.asyncio
async def test_update_password(set_http_conn,create_user):
    passwd_payload = {"current_password":"qwerty","new_password":"awwman"}
    
    passwd_response = await set_http_conn.put("/user/update/password",json=passwd_payload)
    assert passwd_response.status_code == status.HTTP_200_OK
    assert passwd_response.json() == {"message":"Password reset successfully!"}

# check for invalid password at password update

@pytest.mark.asyncio
async def test_incorrect_password(set_http_conn,create_user):
    invalid_passwd_payload = {"current_password":"qwert","new_password":"awwman"}

    invalid_passwd_response = await set_http_conn.put("/user/update/password",json=invalid_passwd_payload)
    assert invalid_passwd_response.status_code == status.HTTP_404_NOT_FOUND
    assert invalid_passwd_response.json() == {"detail":"User not found. Invalid Password"}

# update phone

@pytest.mark.asyncio
async def test_phone_update(set_http_conn,create_user):
    phone_payload = {"phone":"+233248554042"}

    phone_respone = await set_http_conn.put("/user/update/phone",json=phone_payload)
    assert phone_respone.status_code == status.HTTP_200_OK

