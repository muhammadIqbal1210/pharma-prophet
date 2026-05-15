from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal
from decimal import Decimal
class ProductBase(BaseModel):
    nama_produk: str
    kategori: Literal["Obat", "Alkes"]
    satuan: Literal["Tablet", "Botol", "Strip", "Pcs"]
    harga_jual: Decimal = Field(..., gt=0)  # Harga jual harus lebih besar dari 0
    stok_saat_ini: int
    stok_minimum: int
    deskripsi: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nama_produk: Optional[str] = None
    kategori: Optional[str] = None
    satuan: Optional[str] = None
    harga_jual: Optional[Decimal] = None
    stok_saat_ini: Optional[int] = None
    stok_minimum: Optional[int] = None
    deskripsi: Optional[str] = None

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
