from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tanggal = Column(DateTime, default=datetime.utcnow)
    total_harga = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    items = relationship("TransactionDetail", back_populates="transaction")

class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    jumlah = Column(Integer, nullable=False)
    harga_satuan = Column(Float, nullable=False)

    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product")
    