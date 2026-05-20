"""
customer_schema.py - Müşteri veri modelleri
"""
from pydantic import BaseModel
from typing import Optional


class CustomerCreate(BaseModel):
    """Yeni müşteri oluşturmak için gerekli alanlar"""
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerUpdate(BaseModel):
    """Müşteri güncellemek için kullanılan model"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None
