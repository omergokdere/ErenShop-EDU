"""
customer_routes.py - Müşteri endpoint'leri
"""
from fastapi import APIRouter, HTTPException
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate
from app.services import customer_service
from app.utils.response import success_response, error_response

router = APIRouter()


@router.get("/customers")
def list_customers():
    """Tüm aktif müşterileri listeler"""
    customers = customer_service.get_all_customers()
    return success_response(
        message=f"{len(customers)} müşteri listelendi.",
        data=customers
    )


@router.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    """ID'ye göre müşteri getirir"""
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=error_response("Müşteri bulunamadı."))
    return success_response(data=customer)


@router.post("/customers", status_code=201)
def create_customer(body: CustomerCreate):
    """Yeni müşteri ekler"""
    customer, error = customer_service.create_customer(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        address=body.address
    )
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Müşteri başarıyla eklendi.", data=customer)


@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, body: CustomerUpdate):
    """Müşteri bilgilerini günceller"""
    customer, error = customer_service.update_customer(
        customer_id=customer_id,
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        address=body.address,
        is_active=body.is_active
    )
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Müşteri güncellendi.", data=customer)


@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    """Müşteriyi pasife alır"""
    success, error = customer_service.delete_customer(customer_id)
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Müşteri silindi.")


@router.get("/customers/{customer_id}/orders")
def get_customer_orders(customer_id: int):
    """Müşteriye ait siparişleri listeler"""
    # Önce müşteri var mı kontrol et
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=error_response("Müşteri bulunamadı."))
    
    orders = customer_service.get_customer_orders(customer_id)
    return success_response(
        message=f"{len(orders)} sipariş listelendi.",
        data=orders
    )
