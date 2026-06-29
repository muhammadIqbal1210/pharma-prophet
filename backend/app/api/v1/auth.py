from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate
from app.services.auth_service import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user
)

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Cek apakah email sudah terdaftar
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    # 2. Hash password
    hashed_pwd = get_password_hash(user.password)
    
    # 3. Buat objek User baru
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pwd,
        nama_lengkap=user.nama_lengkap,
        role=user.role,
        is_active=True # Memastikan default user baru adalah aktif jika menggunakan soft delete
    )
    
    # 4. Simpan ke database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User berhasil dibuat"}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email atau password salah"
        )
    
    # Tambahan Opsional: Cek jika akun dinonaktifkan (soft-deleted)
    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akun Anda telah dinonaktifkan"
        )
    
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email atau password salah"
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    
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

# Mendapatkan semua user (Hanya menampilkan yang aktif jika memakai soft delete)
@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Jika model User sudah memiliki field 'is_active', gunakan filter ini:
    # users = db.query(User).filter(User.is_active == True).all()
    users = db.query(User).all()
    return users

# Mendapatkan satu user berdasarkan ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return db_user

@router.put("/users/{user_id}")
def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    if updated_data.email != db_user.email:
        email_exists = db.query(User).filter(User.email == updated_data.email).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
        db_user.email = updated_data.email

    db_user.username = updated_data.username
    db_user.nama_lengkap = updated_data.nama_lengkap
    db_user.role = updated_data.role
    
    if updated_data.password:
        db_user.password = get_password_hash(updated_data.password)
    
    db.commit()
    db.refresh(db_user)
    return {"message": "Data user berhasil diperbarui"}

# --- SEKSI PERBAIKAN: SOFT DELETE BERJALAN DI SINI ---
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Anda tidak dapat menghapus diri sendiri")

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    # Pendekatan Soft Delete: Mengecek apakah kolom 'is_active' tersedia di model database Anda
    if hasattr(db_user, 'is_active'):
        db_user.is_active = False
        db.commit()
        return {"message": f"User dengan ID {user_id} berhasil dinonaktifkan (Soft Delete)"}
    
    # Jalur Cadangan (Hard Delete): Jika model database Anda benar-benar belum memiliki kolom 'is_active'
    # Catatan: Ini akan tetap memicu error jika user terkait masih punya data transaksi!
    else:
        db.delete(db_user)
        db.commit()
        return {"message": f"User dengan ID {user_id} terhapus permanen secara fisik"}