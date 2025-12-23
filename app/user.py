from fastapi import APIRouter,HTTPException,status,Depends
from app.models import User
from sqlalchemy import select,update,delete
from app.database import db_injection
from routers.auth import get_user
from app.schemas import CreateUser,CreateResponse,UserUpdate,UpdatePassword,UpdatePhone
from typing import Annotated
from routers.passhashing  import Hash

router = APIRouter(prefix="/user",tags=["User"])

cc_user = Annotated[dict,Depends(get_user)]    # current user injection

# craete a user

@router.post("/create",response_model=CreateResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user:CreateUser,db:db_injection):
    user_create = User(first_name=user.first_name,last_name=user.last_name,email=user.email,\
                      username=user.username, hashed_password=Hash.hash_passwd(user.password),phone=user.phone)
    db.add(user_create)
    await db.commit()
    await db.refresh(user_create)
    return user_create


# get user

@router.get("/me",response_model=CreateResponse,status_code=status.HTTP_200_OK)
async def get_me(db:db_injection,current_user:cc_user):
    user_query = select(User).where(User.id==current_user["id"])
    user_result = await db.execute(user_query)
    user_get = user_result.scalars().first()

    if not user_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User account not found")
    return user_get

# update user

@router.put("/update/me",response_model=CreateResponse,status_code=status.HTTP_200_OK)
async def update_me(user_update:UserUpdate,db:db_injection,current_user:cc_user):
    update_query = update(User).where(User.id==current_user["id"]).values(**user_update.model_dump(exclude_unset=True))\
                                                                        .execution_options(synchronize_session="fetch")
    to_update = await db.execute(update_query)
    if to_update.rowcount==0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Can only update your own account")
    
    await db.commit()
    new_update = select(User).where(User.id==current_user["id"])
    me_update = await db.execute(new_update)
    return_update = me_update.scalars().first() 
    return return_update
    
# update password

@router.put("/update/password",status_code=status.HTTP_200_OK)
async def change_password(db:db_injection,pwd:UpdatePassword,current_user:cc_user):
    passwd_query = select(User).where(User.id==current_user["id"])
    stmt = await db.execute(passwd_query)
    get_detail = stmt.scalars().first()
    
    if not get_detail or not Hash.verify(pwd.current_password,get_detail.hashed_password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found. Invalid Password")
    
    reset_passwd = Hash.hash_passwd(pwd.new_password)
    get_detail.hashed_password=reset_passwd
    await db.commit()
    await db.refresh(get_detail)
    return {"message":"Password reset successfully!"}


 # update phone number

@router.put("/update/phone",response_model=CreateResponse,status_code=status.HTTP_200_OK)
async def update_phone(ph:UpdatePhone,db:db_injection,current_user:cc_user):
    phone_query = update(User).where(User.id==current_user["id"]).values(**ph.model_dump(exclude_unset=True))
    phone_qry = phone_query.execution_options(synchronize_session="fetch")
    get_user_phone = await db.execute(phone_qry)
    if get_user_phone.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found. Can only update your own phone number")
    
    await db.commit()
    new_phone = select(User).where(User.id==current_user["id"])
    new_phone_user = await db.execute(new_phone)
    get_phone = new_phone_user.scalars().first()
    return get_phone

# delete user

@router.delete("/delete/me",status_code=status.HTTP_200_OK)
async def delete_me(current_user:cc_user,db:db_injection):
    delete_qry = select(User).where(User.id==current_user["id"])
    delete_exec = await db.execute(delete_qry)
    get_the_user = delete_exec.scalars().first()

    if not get_the_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Can only delete your own account")
     
    delete_query = delete(User).where(User.id==current_user["id"])
    to_delete = await db.execute(delete_query)
    if to_delete.rowcount==0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Can only delete your own account")
    
    await db.commit()
    return {"message":"User deleted successfully!"}

