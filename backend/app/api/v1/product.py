from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Cek apakah nama produk sudah ada supaya tidak duplikat
    db_product = db.query(Product).filter(Product.nama_produk == product.nama_produk).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Produk dengan nama ini sudah ada")
    
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product

@router.get("/", response_model=list[ProductResponse])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    for key, value in product_update.model_dump().items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

# @router.patch("/{product_id}/update-stock")
# def update_stock(product_id: int, tambahan_stok: int, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
    
#     if not product:
#         raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    
#     # Tambahkan stok yang ada dengan jumlah baru
#     product.stok_saat_ini += tambahan_stok
    
#     db.commit()
#     db.refresh(product)
    
#     return {
#         "message": f"Stok {product.nama_produk} berhasil diperbarui",
#         "stok_baru": product.stok_saat_ini
#     }

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    db.delete(product)
    db.commit()
    return {"message": "Produk berhasil dihapus"}