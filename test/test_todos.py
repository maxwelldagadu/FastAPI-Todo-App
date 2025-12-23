from fastapi import status
import pytest


# test get all todo

@pytest.mark.asyncio
async def test_get_a_all_todo(set_http_conn,todo_create):
    all_todo = await set_http_conn.get("todos/all")

    assert all_todo.status_code == status.HTTP_200_OK
    assert all_todo.json() == [{"id":1,"title":"Testing",
                               "description":"Application Testing",
                                "complete":False,"priority":5,"user_id":1}
    ]

# test make a todo

@pytest.mark.asyncio
async def test_create_a_todo(set_http_conn):

    payload =  {"id":1,"title":"Testing",
                 "description":"Application Testing",
                "complete":False,"priority":5,"user_id":1}
    
    post_response =  await set_http_conn.post("/todos/create",json=payload)
    assert post_response.status_code == status.HTTP_200_OK
    assert post_response.json() == payload

# get a single todo

@pytest.mark.asyncio
async def test_get_a_todo(set_http_conn,todo_create):
    get_todo = await set_http_conn.get("/todos/get/1")

    assert get_todo.status_code == status.HTTP_200_OK
    assert get_todo.json() == {"id":1,"title":"Testing",
                              "description":"Application Testing",
                               "complete":False,"priority":5,"user_id":1}
    
# test against a non existed todo

@pytest.mark.asyncio
async def test_get_a_non_existed_todo(set_http_conn):
    non_exist_response = await set_http_conn.get("/todos/get/50")

    assert non_exist_response.status_code == status.HTTP_404_NOT_FOUND
    assert non_exist_response.json() == {"detail":"Todo with ID 50 not found"}

# test updating a todo

@pytest.mark.asyncio
async def test_update_todo(set_http_conn,todo_create):  
    update_payload = {"priority":5,"title":"Asyncio Testing"}
    update_response = await set_http_conn.put("/todos/update/1",json=update_payload)
    
    assert update_response.status_code == status.HTTP_200_OK

# verify todo exist before update

@pytest.mark.asyncio
async def test_verify_todo_exist(set_http_conn,todo_create):
    to_update = {"priority":5,"title":"Asyncio Testing"}
    verify_todo = await set_http_conn.put("/todos/update/10",json=to_update)

    assert verify_todo.status_code == status.HTTP_404_NOT_FOUND
    assert verify_todo.json() == {"detail":"Todo ID 10 not found. You can only update your own todos"}

# delete todo

@pytest.mark.asyncio
async def test_delete_todo(set_http_conn,todo_create):
    delete_response = await set_http_conn.delete("/todos/delete/1")

    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json() == {"message":"Todo ID 1 successfully deleted"}

# verify id before delete todo

@pytest.mark.asyncio
async def test_check_todo_before_delete(set_http_conn,todo_create):
    check_response = await set_http_conn.delete("/todos/delete/78")

    assert check_response.status_code == status.HTTP_404_NOT_FOUND
    assert check_response.json() == {"detail":"Todo ID 78 not found"}
                                               


