from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    tanggal = Column(DateTime, default=datetime.utcnow)
    total_harga = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id")) # Admin who made the purchase
    supplier_name = Column(String(255), nullable=True) # Optional supplier name
    items = relationship("PurchaseDetail", back_populates="purchase")

class PurchaseDetail(Base):
    __tablename__ = "purchase_details"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    jumlah = Column(Integer, nullable=False)
    harga_satuan = Column(Float, nullable=False) # This is the cost price (harga beli)

    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product")
