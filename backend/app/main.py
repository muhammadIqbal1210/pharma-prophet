from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import router utama yang menggabungkan semua sub-router
from app.api.v1.router import api_router
from app.models import user, product
from app.database.session import engine, Base

app = FastAPI(
    title="Apotek PharmaCast API",
    description="Sistem Manajemen Apotek dengan Prediksi Stok Otomatis (Prophet)",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
# 1. Konfigurasi CORS
# Agar Nuxt.js (frontend) bisa berkomunikasi dengan FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Di produksi, ganti dengan URL Nuxt kamu (misal: http://localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Menghubungkan Router Utama
# Semua endpoint akan dimulai dengan /api/v1
app.include_router(api_router, prefix="/api/v1")

# 3. Endpoint Dasar untuk Cek Health
@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "PharmaCast API is Online",
        "docs": "/docs"
    }

# Jika ingin menjalankan langsung via python app/main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)