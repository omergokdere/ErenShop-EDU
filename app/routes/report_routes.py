"""
report_routes.py - Raporlama endpoint'leri
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services import report_service
from app.utils.response import success_response, error_response

router = APIRouter()


@router.get("/reports/daily-sales")
def daily_sales(date: Optional[str] = Query(None, description="Tarih: YYYY-MM-DD formatında. Boş bırakılırsa bugün.")):
    """Günlük satış raporu"""
    data = report_service.get_daily_sales(date_str=date)
    return success_response(
        message="Günlük satış raporu.",
        data=data
    )


@router.get("/reports/top-products")
def top_products(limit: int = Query(10, description="Kaç ürün listelesin?")):
    """En çok satılan ürünler"""
    data = report_service.get_top_products(limit=limit)
    return success_response(
        message=f"En çok satılan {limit} ürün.",
        data=data
    )


@router.get("/reports/customer-summary/{customer_id}")
def customer_summary(customer_id: int):
    """Müşteri sipariş özeti"""
    data = report_service.get_customer_summary(customer_id)
    if not data:
        raise HTTPException(status_code=404, detail=error_response("Müşteri bulunamadı."))
    return success_response(data=data)


@router.get("/reports/category-sales")
def category_sales():
    """Kategori bazlı satış özeti"""
    data = report_service.get_category_sales()
    return success_response(
        message="Kategori satış raporu.",
        data=data
    )


@router.get("/reports/low-stock-products")
def low_stock_products(threshold: int = Query(10, description="Stok eşik değeri")):
    """Stoğu azalan ürünler"""
    data = report_service.get_low_stock_products(threshold=threshold)
    return success_response(
        message=f"Stoğu {threshold} veya altında olan {len(data)} ürün.",
        data=data
    )
