from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    category: str

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True

from datetime import date, time

class SaleCreate(BaseModel):
    product_id: int
    sale_date: date
    sale_time: time
    quantity_sold: int

class SaleResponse(BaseModel):
    id: int
    product_id: int
    sale_date: date
    sale_time: time
    quantity_sold: int

    class Config:
        from_attributes = True
