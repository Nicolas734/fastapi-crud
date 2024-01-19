from pydantic import BaseModel, EmailStr, constr



class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: constr(min_length=4)



class ResponseCreateUser(BaseModel):
    id: int
    email: EmailStr

    class Config():
        orm_mode = True


class ResponseGetUser(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname:str

    class Config():
        orm_mode = True