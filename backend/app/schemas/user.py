# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    nama_lengkap: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Data yang KELUAR (Response) 
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    nama_lengkap: str
    role: str

    class Config:
        from_attributes = True