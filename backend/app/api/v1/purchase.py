from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.purchase import Purchase, PurchaseDetail
from app.models.product import Product
from app.models.user import User
from app.services.auth_service import get_current_user
from sqlalchemy.orm import joinedload
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from typing import List
from sqlalchemy import func


router = APIRouter()

@router.post("/", response_model=PurchaseResponse)
def create_purchase(data: PurchaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_all = 0
    
    # 1. Inisialisasi Transaksi Pembelian
    new_purchase = Purchase(
        total_harga=0,
        supplier_name=data.supplier_name,
        user_id=current_user.id
    )
    db.add(new_purchase)
    db.flush() 

    for item in data.items:
        # 2. Cari Produk
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Produk ID {item.product_id} tidak ditemukan")
            
        # 3. Hitung Keuangan (berdasarkan harga beli/satuan dari input)
        subtotal = item.harga_satuan * item.jumlah
        total_all += subtotal
        
        # 4. LANGSUNG TAMBAH STOK DI TABEL PRODUCT
        product.stok_saat_ini += item.jumlah
        
        # 5. Simpan Detail untuk Nota Pembelian
        detail = PurchaseDetail(
            purchase_id=new_purchase.id,
            product_id=item.product_id,
            jumlah=item.jumlah,
            harga_satuan=item.harga_satuan
        )
        db.add(detail)

    # 6. Update Total Akhir di Nota
    new_purchase.total_harga = total_all
    
    db.commit()
    db.refresh(new_purchase)
    return new_purchase

@router.get("/", response_model=List[PurchaseResponse])
def get_all_purchases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Purchase).options(joinedload(Purchase.items))
    if current_user.role != "admin":
        query = query.filter(Purchase.user_id == current_user.id)
    return query.all()

@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase_detail(purchase_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Pembelian tidak ditemukan")
    if current_user.role != "admin" and purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak diizinkan melihat pembelian ini")
    return purchase

@router.put("/{purchase_id}", response_model=PurchaseResponse)
def update_purchase(purchase_id: int, data: PurchaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    purchase = db.query(Purchase).options(joinedload(Purchase.items)).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Pembelian tidak ditemukan")
    if current_user.role != "admin" and purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak diizinkan mengedit pembelian ini")

    # Revert stok lama
    for item in purchase.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stok_saat_ini -= item.jumlah

    # Hapus item lama
    for item in list(purchase.items):
        db.delete(item)

    # Tambah item baru & hitung ulang total
    total_all = 0
    purchase.supplier_name = data.supplier_name

    for new_item in data.items:
        product = db.query(Product).filter(Product.id == new_item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Produk ID {new_item.product_id} tidak ditemukan")

        subtotal = new_item.harga_satuan * new_item.jumlah
        total_all += subtotal
        product.stok_saat_ini += new_item.jumlah

        detail = PurchaseDetail(
            purchase_id=purchase.id,
            product_id=new_item.product_id,
            jumlah=new_item.jumlah,
            harga_satuan=new_item.harga_satuan
        )
        db.add(detail)

    purchase.total_harga = total_all
    db.commit()
    db.refresh(purchase)
    return purchase

@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Pembelian tidak ditemukan")
    if current_user.role != "admin" and purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak diizinkan menghapus pembelian ini")
    # Restore stock levels
    for item in purchase.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stok_saat_ini += item.jumlah
    # Delete purchase details and the purchase record
    for item in list(purchase.items):
        db.delete(item)
    db.delete(purchase)
    db.commit()
    return {"message": "Pembelian berhasil dihapus"}

