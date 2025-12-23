from routers.auth import get_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import APIRouter,status,Request,Path
from app.database import db_injection
from app.models import Todos
from sqlalchemy import select


router = APIRouter(prefix="/todos", tags=["Todos"])

### Jinja2 set-up  ###

# jInja2 html template access

templates = Jinja2Templates(directory="templates")

# redirect user to login page function

async def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

# all todos page

@router.get("/todos-page",status_code=status.HTTP_200_OK)
async def todos_page(request:Request,db:db_injection):
    try:

        token_access = await get_user(request.cookies.get("access_token"))
        if not token_access:
            return await redirect_to_login()
        access_query = select(Todos).where(Todos.user_id==token_access["id"])
        access = await db.execute(access_query)
        access_todos = access.scalars().all()
        return templates.TemplateResponse("todos.html",{"request":request,"todos":access_todos,"user": token_access})
    
    except :
        return await redirect_to_login()

# create a todo.....page

@router.get("/add-todos-page",status_code=status.HTTP_200_OK)
async def todo_page(request:Request):
    try:
        access_token = await get_user(request.cookies.get("access_token"))
        if not access_token:
            return await redirect_to_login()
        return templates.TemplateResponse("add-todo.html",{"request":request,"user":access_token})
    except:
        return await redirect_to_login()


# update/edit todo page

@router.get("/edit-todos-page/{todo_id}",status_code=status.HTTP_200_OK)
async def todo_page(request:Request,db:db_injection,todo_id:int=Path(gt=0)):
    user_cookie = get_user(request.cookies.get("access_token"))
    try:
        if not user_cookie:
            return await redirect_to_login()

        cookie_query = select(Todos).where(Todos.id == todo_id) 
        cookie_exec = await db.execute(cookie_query)
        get_that_todo = cookie_exec.scalars().first()
        return templates.TemplateResponse("edit-todo.html",{"request":request,"user":user_cookie,"todo":get_that_todo})
    except ValueError as err:
        return f"{err}"

# 