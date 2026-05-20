"""
order_routes.py - Sipariş endpoint'leri
"""
from fastapi import APIRouter, HTTPException
from app.schemas.order_schema import OrderFromCart, OrderStatusUpdate
from app.services import order_service
from app.utils.response import success_response, error_response

router = APIRouter()


@router.post("/orders/create-from-cart", status_code=201)
def create_order_from_cart(body: OrderFromCart):
    """
    Müşterinin sepetini siparişe dönüştürür.
    Transaction kullanılarak stok düşme işlemi gerçekleştirilir.
    """
    order, error = order_service.create_order_from_cart(customer_id=body.customer_id)
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Sipariş başarıyla oluşturuldu.", data=order)


@router.get("/orders")
def list_orders():
    """Tüm siparişleri listeler"""
    orders = order_service.get_all_orders()
    return success_response(
        message=f"{len(orders)} sipariş listelendi.",
        data=orders
    )


@router.get("/orders/customer/{customer_id}")
def get_orders_by_customer(customer_id: int):
    """Müşteriye ait siparişleri listeler"""
    orders = order_service.get_orders_by_customer(customer_id)
    return success_response(
        message=f"{len(orders)} sipariş listelendi.",
        data=orders
    )


@router.get("/orders/by-number/{order_number}")
def get_order_by_number(order_number: str):
    """Sipariş numarasına göre sipariş detayını getirir"""
    order = order_service.get_order_by_number(order_number)
    if not order:
        raise HTTPException(status_code=404, detail=error_response("Sipariş bulunamadı."))
    return success_response(data=order)


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    """Sipariş detayını getirir"""
    order = order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=error_response("Sipariş bulunamadı."))
    return success_response(data=order)


@router.put("/orders/{order_id}/status")
def update_order_status(order_id: int, body: OrderStatusUpdate):
    """Sipariş durumunu günceller"""
    order, error = order_service.update_order_status(order_id, body.status)
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Sipariş durumu güncellendi.", data=order)
