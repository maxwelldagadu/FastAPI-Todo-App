from fastapi import APIRouter,HTTPException,status,Path,Request
from app.models import Todos
from sqlalchemy import select,delete,update
from app.schemas import TodoActivity,UpdateTodo
from app.database import db_injection
from .user import cc_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/todos", tags=["Todos"])    


# get all todos

@router.get("/all",status_code=status.HTTP_200_OK)
async def get_todos(db:db_injection,current_user:cc_user):
    result_query = select(Todos).where(Todos.user_id==current_user["id"])
    result = await db.execute(result_query)
    get_result = result.scalars().all()

    if not result or not (get_result):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No todos found")
    
    return get_result

# get a todo

@router.get("/get/{todo_id}",status_code=status.HTTP_200_OK)
async def get_a_todo(db:db_injection,current_user:cc_user,todo_id:int=Path(gt=0)):
    a_todo = select(Todos).where(Todos.id==todo_id)
    the_todo = await db.execute(a_todo)
    single_todo = the_todo.scalars().first()

    if not single_todo or not (single_todo.user_id == current_user["id"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with ID {todo_id} not found")
    
    return single_todo

# make a todo

@router.post("/create",status_code=status.HTTP_200_OK)
async def write_todo(activity:TodoActivity,db:db_injection,current_user:cc_user):
    our_todo = Todos(title=activity.title,description=activity.description,priority=activity.priority,user_id=current_user["id"])

    db.add(our_todo)
    await db.commit()
    await db.refresh(our_todo)
    return our_todo

# update todo

@router.put("/update/{todo_id}",status_code=status.HTTP_200_OK)
async def update_todo(db:db_injection,td_update:UpdateTodo,current_user:cc_user,todo_id:int=Path(gt=0)):
    todo_update = update(Todos).where(Todos.id==todo_id).values(**td_update.model_dump(exclude_unset=True))\
                                                            .execution_options(asynchronize_session="fetch")
    update_todo = await db.execute(todo_update)

    updating = select(Todos).where(Todos.id==todo_id)
    to_execute = await db.execute(updating)
    update_tod = to_execute.scalars().first()

    if update_todo.rowcount == 0 or not (update_tod.user_id==current_user["id"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo ID {todo_id} not found. You can only update your own todos")
    await db.commit()
    return update_tod

# delete todo

@router.delete("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def delete_todo(db:db_injection,current_user:cc_user,todo_id:int=Path(gt=0)):
    to_del_qry= select(Todos).where(Todos.id==todo_id)
    del_execute = await db.execute(to_del_qry)
    to_del_todo = del_execute.scalars().first()
    
    if not to_del_todo or not (to_del_todo.user_id==current_user["id"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo ID {todo_id} not found")
    
    delete_query = delete(Todos).where(Todos.id==todo_id)
    delete_td = await db.execute(delete_query)
    if delete_td.rowcount==0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You can only delete your own todos")

    await db.commit()
    return {"message":f"Todo ID {todo_id} successfully deleted"}
