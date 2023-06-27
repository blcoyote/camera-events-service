from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str

    class Config:
        orm_mode = True

class UserGet(User):
    id: str
    disabled: bool

class UserInDB(UserGet):
    hashed_password: str

class UserCreate(User):
    password: str