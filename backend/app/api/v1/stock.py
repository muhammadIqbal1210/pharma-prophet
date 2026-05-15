from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.stock import Stock
from app.models.product import Product
from app.schemas.stock import StockCreate, StockResponse

router = APIRouter()

@router.post("/", response_model=StockResponse)
def create_stock_mutation(data: StockCreate, db: Session = Depends(get_db)):
    # 1. Cek Produk
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    # 2. Logika Update Stok di Tabel Product
    if data.type == "Masuk":
        product.stok_saat_ini += data.jumlah
    else: # Jika Keluar
        if product.stok_saat_ini < data.jumlah:
            raise HTTPException(status_code=400, detail="Stok tidak mencukupi untuk pengeluaran")
        product.stok_saat_ini -= data.jumlah
    
    # 3. Simpan Riwayat Mutasi
    new_mutation = Stock(
        product_id=data.product_id,
        type=data.type,
        jumlah=data.jumlah,
        expired_date=data.expired_date,
        deskripsi=data.deskripsi
    )
    
    db.add(new_mutation)
    db.commit()
    db.refresh(new_mutation)
    return new_mutation

@router.get("/product/{product_id}", response_model=list[StockResponse])
def get_stock_history(product_id: int, db: Session = Depends(get_db)):
    # Cek Produk
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    # Ambil Riwayat Mutasi untuk Produk Tersebut
    history = db.query(Stock).filter(Stock.product_id == product_id).order_by(Stock.tanggal_update.desc()).all()
    return history

@router.get("/{stock_id}", response_model=StockResponse)
def get_stock_by_id(stock_id: int, db: Session = Depends(get_db)):
    stock_entry = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock_entry:
        raise HTTPException(status_code=404, detail="Mutasi stok tidak ditemukan")
    return stock_entry

@router.get("/", response_model=list[StockResponse])
def get_all_stock_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    history = db.query(Stock).offset(skip).limit(limit).all()
    return history

@router.put("/{stock_id}", response_model=StockResponse)
def update_stock_entry(stock_id: int, stock_update: StockCreate, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Mutasi stok tidak ditemukan")
    
    # Cek Produk
    product = db.query(Product).filter(Product.id == stock_update.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    # Revert Stok Lama
    if stock.type == "Masuk":
        product.stok_saat_ini -= stock.jumlah
    else:
        product.stok_saat_ini += stock.jumlah
    
    # Update dengan Data Baru
    for key, value in stock_update.model_dump().items():
        setattr(stock, key, value)
    
    # Terapkan Perubahan Stok Baru
    if stock_update.type == "Masuk":
        product.stok_saat_ini += stock_update.jumlah
    else:
        if product.stok_saat_ini < stock_update.jumlah:
            raise HTTPException(status_code=400, detail="Stok tidak mencukupi untuk pengeluaran")
        product.stok_saat_ini -= stock_update.jumlah
    
    db.commit()
    db.refresh(stock)
    return stock

@router.delete("/{stock_id}")
def delete_stock_entry(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Mutasi stok tidak ditemukan")
    
    # Cek Produk
    product = db.query(Product).filter(Product.id == stock.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    # Revert Stok Sesuai Jenis Mutasi yang Dihapus
    if stock.type == "Masuk":
        product.stok_saat_ini -= stock.jumlah
    else:
        product.stok_saat_ini += stock.jumlah
    
    db.delete(stock)
    db.commit()
    
    return {"message": f"Mutasi stok dengan ID {stock_id} berhasil dihapus"}