from fastapi import APIRouter,Depends,HTTPException,status,Request
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timezone,timedelta
from jose import jwt,JWTError
from app.database import db_injection
from sqlalchemy import select
from .passhashing import Hash
import os
from app.models import User
from fastapi.templating import Jinja2Templates

load_dotenv()

router = APIRouter(prefix="/auth",tags=["authentication"])

#bearer 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

# jinja2 html template access
templates = Jinja2Templates(directory="templates")

### pages ###

# login page

@router.get("/login-page")   
async def login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

# register page

@router.get("/register-page")    
async def register_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})


# set/encode token

def login_token(email:str,id:int):
    token = {"sub":email,"id":id}
    expiry = datetime.now(timezone.utc) + timedelta(minutes=60)
    token.update({"exp":expiry})
    jwt_token = jwt.encode(token,os.getenv("SECRET_KEY"),algorithm=os.getenv("ALGORITHM"))
    return jwt_token


#create token 

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(db:db_injection,user_form:str=Depends(OAuth2PasswordRequestForm)):
    user_query = select(User).where(User.email==user_form.username)
    get_user = await db.execute(user_query)
    client = get_user.scalars().first()
    if not client or not Hash.verify(user_form.password,client.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid User Credentials")
    
    user_token = login_token(client.email,client.id)
    return {"token_type":"Bearer","access_token":user_token}

# decode jwt token

async def get_user(jwt_token:str=Depends(oauth2_bearer)):
    try:
        decode_token = jwt.decode(jwt_token,os.getenv("SECRET_KEY"),algorithms=[os.getenv("ALGORITHM")])
        get_email = decode_token.get("sub")
        get_id = decode_token.get("id")
        if get_email is None or get_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid User Credentials")
        
        return {"id":get_id}
    
    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"{err}")



