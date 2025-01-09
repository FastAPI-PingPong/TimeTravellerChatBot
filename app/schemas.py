from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserCreateResposne(BaseModel):
    username: str
    id: int
