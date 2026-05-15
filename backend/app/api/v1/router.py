from fastapi import APIRouter
from app.api.v1 import auth # products, predictions  Import semua file di v1

api_router = APIRouter()

# Daftarkan semua sub-router ke sini
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(products.router, prefix="/products", tags=["Inventory"])
# api_router.include_router(predictions.router, prefix="/predictions", tags=["ML Predictions"])