from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.transaction import Transaction, TransactionDetail
from app.models.product import Product
from app.schemas.transaction import TransactionCreate, TransactionResponse

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