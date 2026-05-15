# app/schemas/user.py
import re

from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    nama_lengkap: str
    role: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        # 1. Cek panjang minimal
        if len(v) < 8:
            raise ValueError('Password minimal harus 8 karakter')
            
        # 2. Cek apakah ada huruf besar
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password harus mengandung minimal satu huruf besar (A-Z)')
            
        # 3. Cek apakah ada angka
        if not re.search(r'[0-9]', v):
            raise ValueError('Password harus mengandung minimal satu angka (0-9)')
            
        # 4. Cek apakah ada karakter spesial/simbol
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError('Password harus mengandung minimal satu simbol (@$!%*?&)')
            
        return v

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