from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# URL Koneksi ke MySQL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Engine: Jembatan ke database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal: Untuk melakukan transaksi (tambah, edit, hapus)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Class induk untuk semua file di folder 'models'
Base = declarative_base()

# Fungsi Dependency Injection untuk Router
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()