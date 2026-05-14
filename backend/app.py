from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import fetch_sales_data
from forecast_logic import run_prophet_forecast
from pydantic import BaseModel
import bcrypt
import mysql.connector

# Inisialisasi FastAPI
app = FastAPI(title="PharmaCast API", description="API Prediksi Stok Obat menggunakan Prophet")

# Setup CORS agar Nuxt.js bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Di produksi, ganti dengan URL Nuxt kamu
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Keamanan Password
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Model Data untuk validasi input (Pydantic)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    nama_lengkap: str
    role: str

def get_password_hash(password: str):
    # Ubah password teks ke format bytes
    pwd_bytes = password.encode('utf-8')
    # Buat salt (pengacak)
    salt = bcrypt.gensalt()
    # Lakukan hashing
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Kembalikan sebagai string agar bisa masuk ke kolom VARCHAR MySQL
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    # Mengecek apakah input user cocok dengan hash di database
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )
# --- 1. ENDPOINT REGISTRASI ---
@app.post("/api/users/register")
async def register(user: UserCreate):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="db_pharmacast")
        cursor = conn.cursor()
        
        # Cek apakah email sudah ada
        cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username sudah terdaftar")
        
        # Hash password sebelum simpan
        hashed_pwd = get_password_hash(user.password)
        
        # Simpan ke Database
        sql = "INSERT INTO users (username,email, password, nama_lengkap, role) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (user.username, user.email, hashed_pwd, user.nama_lengkap, user.role))
        
        conn.commit()
        conn.close()
        return {"message": "User berhasil dibuat!"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# --- 2. ENDPOINT LOGIN ---
@app.post("/api/users/login")
async def login(email: str, password: str):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="db_pharmacast")
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not verify_password(password, user['password']):
            raise HTTPException(status_code=401, detail="Email atau password salah")
        
        return {
            "message": "Login berhasil",
            "user": {
                "id": user['id'],
                "email": user['username'], # Asumsi email disimpan di kolom username
                "nama_lengkap": user['nama_lengkap'],
                "username": user['username'],
                "role": user['role']
            }
        }
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/predict/{product_id}")
async def predict(product_id: int):
    try:
        # 1. Ambil data dari database
        raw_data = fetch_sales_data(product_id)
        
        if not raw_data or len(raw_data) < 10:
            raise HTTPException(status_code=400, detail="Data historis tidak cukup")
        
        # 2. Jalankan prediksi (Prophet)
        forecast_output = run_prophet_forecast(raw_data)
        
        return {
            "status": "success",
            "product_id": product_id,
            "accuracy_score": forecast_output['accuracy'],
            "data": forecast_output['predictions']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
