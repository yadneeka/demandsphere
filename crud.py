from sqlalchemy.orm import Session
import models
import schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, category=product.category)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(
        product_id=sale.product_id,
        sale_date=sale.sale_date,
        sale_time=sale.sale_time,
        quantity_sold=sale.quantity_sold
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session):
    return db.query(models.Sale).all()

def get_sales_by_product(db: Session, product_id: int):
    return db.query(models.Sale).filter(models.Sale.product_id == product_id).all()

def delete_sale(db: Session, sale_id: int):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if sale:
        db.delete(sale)
        db.commit()
    return sale

from sqlalchemy import func

def get_daily_sales_by_product(db: Session, product_id: int):
    return (
        db.query(
            models.Sale.sale_date,
            func.sum(models.Sale.quantity_sold).label("total_quantity")
        )
        .filter(models.Sale.product_id == product_id)
        .group_by(models.Sale.sale_date)
        .order_by(models.Sale.sale_date)
        .all()
    )
