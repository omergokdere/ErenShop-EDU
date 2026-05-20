"""
payment_schema.py - Ödeme veri modelleri
"""
from pydantic import BaseModel, Field


class MockPayment(BaseModel):
    """Mock ödeme işlemi için gerekli alanlar"""
    order_id: int = Field(alias="orderId")
    payment_type: str = Field(alias="paymentType")
    amount: float
    force_fail: bool = Field(default=False, alias="forceFail")
    # force_fail=True → ödemeyi başarısız simüle et

    class Config:
        populate_by_name = True
