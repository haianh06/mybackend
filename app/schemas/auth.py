from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    tenant_id: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str