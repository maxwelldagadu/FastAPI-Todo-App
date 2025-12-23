from pydantic import BaseModel,Field,EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class TodoActivity(BaseModel):    # post a todo 

    title: str = Field(...,min_length=1)
    description: str = Field(...,min_length=1)
    priority: int = Field(...,gt=0,lt=6)


class UpdateTodo(BaseModel):    # update a todo

    title: str = Field(...,min_length=1)
    description: str = Field(...,min_length=1)
    
    
class CreateUser(BaseModel):    # craete a user

    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr = Field(...)
    password: str = Field(...)
    phone: PhoneNumber = Field(...)
    username: str = Field(...)

class CreateResponse(BaseModel):    # response for create_user,get_user,update_phone and update_user route
  
    first_name: str
    last_name: str 
    email: EmailStr 
    is_active:bool
    phone : str
    username: str
    model_config = {"from_attributes":True}
    



class UserUpdate(BaseModel):    # update user

    first_name: str = Field(...,min_length=1)
    last_name: str = Field(...,min_length=1)
    email: EmailStr = Field(...)


class UpdatePassword(BaseModel): # update password
    
    current_password: str
    new_password: str = Field(...)


class UpdatePhone(BaseModel):
    phone: PhoneNumber = Field(...)