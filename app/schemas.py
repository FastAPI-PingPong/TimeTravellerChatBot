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


class SessionCreate(BaseModel):
    year: int
    location: str
    persona: str


class SessionCreateResponse(BaseModel):
    id: int


class ChatCreate(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str
