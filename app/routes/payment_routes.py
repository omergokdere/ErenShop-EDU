"""
payment_routes.py - Ödeme endpoint'leri
"""
from fastapi import APIRouter, HTTPException
from app.schemas.payment_schema import MockPayment
from app.services import payment_service
from app.utils.response import success_response, error_response

router = APIRouter()


@router.post("/payments/mock-pay", status_code=200)
def mock_pay(body: MockPayment):
    """
    Mock ödeme işlemi.
    forceFail=true gönderirsen ödeme başarısız simüle edilir.
    Ödeme başarılıysa sipariş durumu 'Paid' olur.
    Başarısızsa 'PaymentFailed' olur.
    """
    result, error = payment_service.process_mock_payment(
        order_id=body.order_id,
        payment_type=body.payment_type,
        amount=body.amount,
        force_fail=body.force_fail
    )
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    
    if result["is_successful"]:
        return success_response(message="Ödeme başarıyla tamamlandı.", data=result)
    else:
        # Ödeme başarısız ama API isteği başarılıydı, bu yüzden 200 dönüyoruz
        # Sadece data içinde is_successful=false gösteririz
        return success_response(message="Ödeme başarısız. Sipariş durumu güncellendi.", data=result)
