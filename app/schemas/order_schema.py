"""
order_schema.py - Sipariş veri modelleri
"""
from pydantic import BaseModel, Field
from typing import Optional


class OrderFromCart(BaseModel):
    """Sepetten sipariş oluşturmak için gerekli alanlar"""
    customer_id: int = Field(alias="customerId")

    class Config:
        populate_by_name = True


class OrderStatusUpdate(BaseModel):
    """Sipariş durumunu güncellemek için kullanılan model"""
    status: str
    # Geçerli durumlar: Pending, Processing, Shipped, Delivered, Cancelled, Paid, PaymentFailed
