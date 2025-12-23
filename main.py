from app.database import create_all_tables
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request,status
from fastapi.responses import RedirectResponse
from app import todo,user
from routers import auth,jinja2_page_rendering
from fastapi.staticfiles import StaticFiles



@asynccontextmanager
async def lifespan(app:FastAPI):
    # startup code
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)


# render to  todo page as home page

@app.get("/",status_code=status.HTTP_200_OK)
async def home_page(request:Request):
    redirect = RedirectResponse(url="/todos/todos-page",status_code=status.HTTP_302_FOUND)
    return redirect

# render bootstrap styling 

app.mount("/static",StaticFiles(directory="static"),name="static")

# routers

app.include_router(todo.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(jinja2_page_rendering.router)