"""
product_routes.py - Ürün endpoint'leri
Path parameter, query parameter kullanımı öğretilir.
"""
from fastapi import APIRouter, HTTPException, Query
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services import product_service
from app.utils.response import success_response, error_response

router = APIRouter()


@router.get("/products")
def list_products():
    """Tüm aktif ürünleri listeler"""
    products = product_service.get_all_products()
    return success_response(
        message=f"{len(products)} ürün listelendi.",
        data=products
    )


@router.get("/products/search")
def search_products(keyword: str = Query(..., description="Arama anahtar kelimesi")):
    """
    Ürünlerde arama yapar.
    Örnek: GET /api/products/search?keyword=mouse
    Query parameter kullanımı öğretilir.
    """
    products = product_service.search_products(keyword)
    return success_response(
        message=f"'{keyword}' için {len(products)} sonuç bulundu.",
        data=products
    )


@router.get("/products/category/{category_id}")
def products_by_category(category_id: int):
    """Kategoriye göre ürünleri listeler"""
    products = product_service.get_products_by_category(category_id)
    return success_response(
        message=f"{len(products)} ürün listelendi.",
        data=products
    )


@router.get("/products/{product_id}")
def get_product(product_id: int):
    """ID'ye göre tek ürün getirir"""
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=error_response("Ürün bulunamadı."))
    return success_response(data=product)


@router.post("/products", status_code=201)
def create_product(body: ProductCreate):
    """Yeni ürün ekler"""
    product, error = product_service.create_product(
        category_id=body.category_id,
        name=body.name,
        description=body.description,
        price=body.price,
        stock=body.stock
    )
    if error:
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Ürün başarıyla eklendi.", data=product)


@router.put("/products/{product_id}")
def update_product(product_id: int, body: ProductUpdate):
    """Ürün bilgilerini günceller"""
    product, error = product_service.update_product(
        product_id=product_id,
        category_id=body.category_id,
        name=body.name,
        description=body.description,
        price=body.price,
        stock=body.stock,
        is_active=body.is_active
    )
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Ürün güncellendi.", data=product)


@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Ürünü pasife alır"""
    success, error = product_service.delete_product(product_id)
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Ürün silindi.")
