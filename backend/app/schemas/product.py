from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal

class ProductBase(BaseModel):
    nama_produk: str
    kategori: Literal["Obat", "Alkes"]
    satuan: Literal["Tablet", "Botol", "Strip", "Pcs"]
    harga_jual: float
    stok_saat_ini: int
    stok_minimum: int
    deskripsi: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nama_produk: Optional[str] = None
    kategori: Optional[str] = None
    satuan: Optional[str] = None
    harga_jual: Optional[float] = None
    stok_saat_ini: Optional[int] = None
    stok_minimum: Optional[int] = None
    deskripsi: Optional[str] = None

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
