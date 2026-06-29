from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.schemas.product import ProductResponse

class PurchaseItemCreate(BaseModel):
    product_id: int
    jumlah: int
    harga_satuan: float

class PurchaseCreate(BaseModel):
    supplier_name: Optional[str] = None
    items: List[PurchaseItemCreate]

class PurchaseDetailSchema(BaseModel):
    id: int
    product_id: int
    jumlah: int
    harga_satuan: float
    product: Optional[ProductResponse] = None 

    model_config = ConfigDict(from_attributes=True)

class PurchaseResponse(BaseModel):
    id: int
    tanggal: datetime
    total_harga: float
    supplier_name: Optional[str] = None
    user_id: Optional[int] = None
    items: List[PurchaseDetailSchema] 

    model_config = ConfigDict(from_attributes=True)
