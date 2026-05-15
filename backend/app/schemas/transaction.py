from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.schemas.product import ProductResponse

class TransactionItemCreate(BaseModel):
    product_id: int
    jumlah: int

class TransactionCreate(BaseModel):
    items: List[TransactionItemCreate]

class TransactionDetailSchema(BaseModel):
    id: int
    product_id: int
    jumlah: int
    harga_satuan: float
    product: Optional[ProductResponse] = None 

    model_config = ConfigDict(from_attributes=True)

class TransactionResponse(BaseModel):
    id: int
    tanggal: datetime
    total_harga: float
    # List detail transaksi yang sekarang sudah ada info produknya
    items: List[TransactionDetailSchema] 

    model_config = ConfigDict(from_attributes=True)