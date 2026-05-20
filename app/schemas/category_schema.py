"""
category_schema.py - Kategori veri modelleri
Pydantic modelleri ile gelen verilerin doğrulanması sağlanır.
"""
from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    """Yeni kategori oluşturmak için gerekli alanlar"""
    name: str
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    """Kategori güncellemek için kullanılan model (tüm alanlar opsiyonel)"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
