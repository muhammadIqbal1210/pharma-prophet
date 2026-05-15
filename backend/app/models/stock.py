from sqlalchemy import Column, Enum, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.session import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    type = Column(Enum("Masuk", "Keluar", name="type_enum"), nullable=False)  # "masuk" atau "keluar"
    jumlah = Column(Integer, nullable=False)
    tanggal_update = Column(DateTime, default=datetime.utcnow)
    expired_date = Column(DateTime, nullable=True)  # Hanya untuk jenis "masuk" (pembelian)
    deskripsi = Column(String(255), nullable=True)  # Opsional, untuk catatan tambahan