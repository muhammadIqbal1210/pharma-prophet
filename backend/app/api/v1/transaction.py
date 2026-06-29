from datetime import date, datetime
from unittest import result
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.transaction import Transaction, TransactionDetail
from app.models.product import Product
from app.models.user import User
from app.services.auth_service import get_current_user
from sqlalchemy.orm import joinedload
from app.schemas.transaction import TransactionCreate, TransactionResponse
from typing import List
from sqlalchemy import func


router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_all = 0
    
    # 1. Inisialisasi Transaksi
    new_transaction = Transaction(total_harga=0, user_id=current_user.id)
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
def get_all_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # .joinedload() memastikan data items dan product diambil sekaligus (Eager Loading)
    query = db.query(Transaction).options(joinedload(Transaction.items))
    if current_user.role != "admin":
        query = query.filter(Transaction.user_id == current_user.id)
    return query.all()

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_detail(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    if current_user.role != "admin" and transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak diizinkan melihat transaksi ini")
    return transaction

@router.get("/report/summary")
def get_sales_report(start_date: date, end_date: date, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from app.models.purchase import Purchase
    # 1. Pastikan ada .label("count") dan .label("total")
    query_sales = db.query(
        func.count(Transaction.id).label("count"),  # Label harus 'count'
        func.sum(Transaction.total_harga).label("total")  # Label harus 'total'
    ).filter(
        func.date(Transaction.tanggal) >= start_date, 
        func.date(Transaction.tanggal) <= end_date
    )
    
    query_purchases = db.query(
        func.count(Purchase.id).label("count"),
        func.sum(Purchase.total_harga).label("total")
    ).filter(
        func.date(Purchase.tanggal) >= start_date, 
        func.date(Purchase.tanggal) <= end_date
    )

    if current_user.role != "admin":
        query_sales = query_sales.filter(Transaction.user_id == current_user.id)
        query_purchases = query_purchases.filter(Purchase.user_id == current_user.id)

    result_sales = query_sales.first()
    result_purchases = query_purchases.first()

    # 2. Sekarang result.total and result.count sudah pasti ada
    total_omzet = result_sales.total if result_sales.total is not None else 0
    total_transaksi = result_sales.count if result_sales.count is not None else 0

    total_pengeluaran = result_purchases.total if result_purchases.total is not None else 0
    total_pembelian = result_purchases.count if result_purchases.count is not None else 0

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_transaksi": total_transaksi,
        "total_omzet": total_omzet,
        "total_pembelian": total_pembelian,
        "total_pengeluaran": total_pengeluaran
    }

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, data: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    if current_user.role != "admin" and transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak diizinkan mengubah transaksi ini")
        
    # 1. Restore the old stock levels temporarily
    for item in transaction.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stok_saat_ini += item.jumlah
            
    # 2. Delete existing transaction detail items
    for item in list(transaction.items):
        db.delete(item)
    db.flush()
    
    # 3. Process new transaction details & deduct new stock
    total_all = 0
    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Produk ID {item.product_id} tidak ditemukan")
            
        if product.stok_saat_ini < item.jumlah:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Stok {product.nama_produk} tidak cukup (Sisa: {product.stok_saat_ini})")
            
        subtotal = product.harga_jual * item.jumlah
        total_all += subtotal
        
        product.stok_saat_ini -= item.jumlah
        
        detail = TransactionDetail(
            transaction_id=transaction.id,
            product_id=item.product_id,
            jumlah=item.jumlah,
            harga_satuan=product.harga_jual
        )
        db.add(detail)
        
    transaction.total_harga = total_all
    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    if current_user.role != "admin" and transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak diizinkan menghapus transaksi ini")
    
    # Restore stock levels
    for item in transaction.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stok_saat_ini += item.jumlah
            
    # Delete details and the transaction itself
    for item in list(transaction.items):
        db.delete(item)
    db.delete(transaction)
    db.commit()
    return {"message": "Transaksi berhasil dihapus"}
