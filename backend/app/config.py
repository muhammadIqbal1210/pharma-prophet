import os
from dotenv import load_dotenv

# Mencari file .env di folder root (backend/.env)

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(basedir, ".env"))

class Settings:
    PROJECT_TITLE: str = "PharmaCast API"
    
    # Database Configuration
    # Format: mysql+mysqlconnector://user:password@host/dbname
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

# Inisialisasi agar bisa langsung di-import
settings = Settings()

