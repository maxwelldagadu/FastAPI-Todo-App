from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,Boolean,Integer,ForeignKey




class Base(DeclarativeBase):
      pass

# todo table

class Todos(Base):

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    priority: Mapped[int] = mapped_column(Integer)
    complete: Mapped[bool] = mapped_column(Boolean,default=False)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("user.id",ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="todo")

class User(Base):
     
     __tablename__ = "user"

     id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
     first_name: Mapped[str] = mapped_column(String)
     last_name: Mapped[str] = mapped_column(String)
     email: Mapped[str] = mapped_column(String,unique=True)
     hashed_password: Mapped[str] = mapped_column(String)
     is_active: Mapped[bool] = mapped_column(Boolean,default=True)
     phone: Mapped[str] = mapped_column(nullable=False)
     username: Mapped[str] = mapped_column(String,unique=True,nullable=False)

     
     todo: Mapped[list["Todos"]]= relationship(back_populates="user",cascade="all,delete-orphan")
     