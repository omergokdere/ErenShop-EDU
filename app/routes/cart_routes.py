"""
cart_routes.py - Sepet endpoint'leri
"""
from fastapi import APIRouter, HTTPException
from app.schemas.cart_schema import CartItemAdd
from app.services import cart_service
from app.utils.response import success_response, error_response

router = APIRouter()


@router.post("/cart/add", status_code=201)
def add_to_cart(body: CartItemAdd):
    """Sepete ürün ekler. Sepet yoksa otomatik oluşturur."""
    cart, error = cart_service.add_to_cart(
        customer_id=body.customer_id,
        product_id=body.product_id,
        quantity=body.quantity
    )
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Ürün sepete eklendi.", data=cart)


@router.get("/cart/{customer_id}")
def get_cart(customer_id: int):
    """Müşterinin sepetini ve toplam tutarını getirir"""
    cart = cart_service.get_cart(customer_id)
    return success_response(data=cart)


@router.delete("/cart/items/{cart_item_id}")
def remove_cart_item(cart_item_id: int):
    """Sepetten tek bir ürünü siler"""
    success, error = cart_service.remove_cart_item(cart_item_id)
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Ürün sepetten çıkarıldı.")


@router.delete("/cart/clear/{customer_id}")
def clear_cart(customer_id: int):
    """Müşterinin sepetini tamamen temizler"""
    success, error = cart_service.clear_cart(customer_id)
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Sepet temizlendi.")
