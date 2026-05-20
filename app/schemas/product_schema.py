"""
product_schema.py - Ürün veri modelleri
"""
from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    """Yeni ürün oluşturmak için gerekli alanlar"""
    category_id: int = Field(alias="categoryId")
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    class Config:
        populate_by_name = True


class ProductUpdate(BaseModel):
    """Ürün güncellemek için kullanılan model"""
    category_id: Optional[int] = Field(default=None, alias="categoryId")
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None

    class Config:
        populate_by_name = True
