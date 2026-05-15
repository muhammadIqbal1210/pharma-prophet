# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate
from app.models.user import User
from app.services.auth_service import get_password_hash
from app.database.session import get_db
from app.schemas.user import UserResponse, UserLogin, UserCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth_service import verify_password, create_access_token

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db = Depends(get_db)):
    # 1. Cek apakah email sudah terdaftar menggunakan SQLAlchemy query
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    # 2. Hash password
    hashed_pwd = get_password_hash(user.password)
    
    # 3. Buat objek User baru dari model SQLAlchemy
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pwd,
        nama_lengkap=user.nama_lengkap,
        role=user.role
    )
    
    # 4. Simpan ke database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User berhasil dibuat "}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # 1. Cari user berdasarkan email
    user = db.query(User).filter(User.email == user_data.email).first()
    
    # 2. Cek apakah user ditemukan
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email atau password salah"
        )
    
    # 3. Verifikasi password yang diinput dengan hash di database
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email atau password salah"
        )
    
    # 4. Jika cocok, buatkan Token JWT
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    
    # 5. Kirim token ke Frontend
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }

# Mendapatkan semua user
@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Mendapatkan satu user berdasarkan ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return db_user

@router.put("/users/{user_id}")
def update_user(user_id: int, updated_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    # Update field
    db_user.username = updated_data.username
    db_user.nama_lengkap = updated_data.nama_lengkap
    db_user.role = updated_data.role
    
    # Jika ingin ganti password, harus di-hash lagi
    db_user.password = get_password_hash(updated_data.password)
    
    db.commit()
    db.refresh(db_user)
    return {"message": "Data user berhasil diperbarui"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    db.delete(db_user)
    db.commit()
    return {"message": f"User dengan ID {user_id} berhasil dihapus"}