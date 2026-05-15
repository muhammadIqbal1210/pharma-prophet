from datetime import date, datetime
from unittest import result
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.transaction import Transaction, TransactionDetail
from app.models.product import Product
from sqlalchemy.orm import joinedload
from app.schemas.transaction import TransactionCreate, TransactionResponse
from typing import List
from sqlalchemy import func


router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    total_all = 0
    
    # 1. Inisialisasi Transaksi
    new_transaction = Transaction(total_harga=0)
    db.add(new_transaction)
    db.flush() 

    for item in data.items:
        # 2. Cari Produk & Validasi Stok
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Produk ID {item.product_id} tidak ditemukan")
            
        if product.stok_saat_ini < item.jumlah:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Stok {product.nama_produk} tidak cukup (Sisa: {product.stok_saat_ini})")
        
        # 3. Hitung Keuangan
        subtotal = product.harga_jual * item.jumlah
        total_all += subtotal
        
        # 4. LANGSUNG POTONG STOK DI TABEL PRODUCT
        product.stok_saat_ini -= item.jumlah
        
        # 5. Simpan Detail untuk Nota
        detail = TransactionDetail(
            transaction_id=new_transaction.id,
            product_id=item.product_id,
            jumlah=item.jumlah,
            harga_satuan=product.harga_jual
        )
        db.add(detail)

    # 6. Update Total Akhir di Nota
    new_transaction.total_harga = total_all
    
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.get("/", response_model=List[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    # .joinedload() memastikan data items dan product diambil sekaligus (Eager Loading)
    return db.query(Transaction).options(joinedload(Transaction.items)).all()

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_detail(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    return transaction

@router.get("/report/summary")
def get_sales_report(start_date: date, end_date: date, db: Session = Depends(get_db)):
    # 1. Pastikan ada .label("count") dan .label("total")
    result = db.query(
        func.count(Transaction.id).label("count"),  # Label harus 'count'
        func.sum(Transaction.total_harga).label("total")  # Label harus 'total'
    ).filter(
        func.date(Transaction.tanggal) >= start_date, 
        func.date(Transaction.tanggal) <= end_date
    ).first()

    # 2. Sekarang result.total dan result.count sudah pasti ada
    total_omzet = result.total if result.total is not None else 0
    total_transaksi = result.count if result.count is not None else 0

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_transaksi": total_transaksi,
        "total_omzet": total_omzet
    }