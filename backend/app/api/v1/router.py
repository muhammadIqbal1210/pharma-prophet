from fastapi import APIRouter
from app.api.v1 import auth, product, stock # predictions  Import semua file di v1

api_router = APIRouter()

# Daftarkan semua sub-router ke sini
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(product.router, prefix="/product", tags=["Product"])
api_router.include_router(stock.router, prefix="/stock", tags=["Stock"])