"""
cart_schema.py - Sepet veri modelleri
"""
from pydantic import BaseModel, Field


class CartItemAdd(BaseModel):
    """Sepete ürün eklemek için gerekli alanlar"""
    customer_id: int = Field(alias="customerId")
    product_id: int = Field(alias="productId")
    quantity: int = Field(ge=1)  # ge=1 → en az 1 adet olmalı

    class Config:
        populate_by_name = True
