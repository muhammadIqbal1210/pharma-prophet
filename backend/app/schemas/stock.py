from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal, Optional

class StockBase(BaseModel):
    product_id: int
    type: Literal["Masuk", "Keluar"]
    jumlah: int 
    expired_date: Optional[datetime] = None
    tanggal_update: datetime
    deskripsi: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockResponse(BaseModel):
    id: int
    product_id: int
    type: str
    jumlah: int
    tanggal_update: datetime
    expired_date: Optional[datetime] = None
    deskripsi: Optional[str]

    model_config = ConfigDict(from_attributes=True)