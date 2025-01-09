from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserCreateResposne(BaseModel):
    username: str
    id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
