from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BookOut(BaseModel):
    id: int
    name: str
    author: Optional[str]=None
    class Config:
        orm_mode = True

class BookPlay(BaseModel):
    play: conint(ge=0, le=3)

class BookPage(BaseModel):
    page: Optional[int]=0

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None



