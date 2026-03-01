from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "DemandSphere Backend Running"}

# Create Product
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

# Get All Products
@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

# Get Single Product
@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Delete Product
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Create Sale
@app.post("/sales", response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, sale)

# Get All Sales
@app.get("/sales", response_model=list[schemas.SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return crud.get_sales(db)

# Get Sales By Product
@app.get("/sales/product/{product_id}", response_model=list[schemas.SaleResponse])
def get_sales_by_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_sales_by_product(db, product_id)

# Delete Sale
@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = crud.delete_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"message": "Sale deleted successfully"}

# Get Daily Aggregated Sales
@app.get("/sales/daily/{product_id}")
def get_daily_sales(product_id: int, db: Session = Depends(get_db)):
    results = crud.get_daily_sales_by_product(db, product_id)

    return [
        {
            "sale_date": r.sale_date,
            "total_quantity": r.total_quantity
        }
        for r in results
    ]
