from sqlalchemy import Column, Enum, Integer, Numeric, String, String, Text
from app.database.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nama_produk = Column(String(255), nullable=False)
    kategori = Column(Enum("Obat", "Alkes", name="kategori_enum"), nullable=False)
    satuan = Column(Enum("Tablet", "Botol", "Strip", "Pcs", name="satuan_enum"), nullable=False)
    harga_jual = Column(Numeric(10, 2), nullable=False)
    stok_saat_ini = Column(Integer, default=0)
    stok_minimum = Column(Integer, default=10) # Alert jika stok < 10
    deskripsi = Column(Text, nullable=True)