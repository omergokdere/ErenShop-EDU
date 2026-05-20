"""
category_routes.py - Kategori endpoint'leri
GET, POST, PUT, DELETE metodları burada tanımlanır.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services import category_service
from app.utils.response import success_response, error_response

router = APIRouter()


@router.get("/categories")
def list_categories():
    """Tüm aktif kategorileri listeler"""
    categories = category_service.get_all_categories()
    return success_response(
        message=f"{len(categories)} kategori listelendi.",
        data=categories
    )


@router.get("/categories/{category_id}")
def get_category(category_id: int):
    """ID'ye göre tek kategori getirir"""
    category = category_service.get_category_by_id(category_id)
    if not category:
        # 404 Not Found - kaynak bulunamadı
        raise HTTPException(status_code=404, detail=error_response("Kategori bulunamadı."))
    return success_response(data=category)


@router.post("/categories", status_code=201)
def create_category(body: CategoryCreate):
    """Yeni kategori ekler"""
    category, error = category_service.create_category(
        name=body.name,
        description=body.description
    )
    if error:
        # 400 Bad Request - geçersiz istek
        raise HTTPException(status_code=400, detail=error_response(error))
    return success_response(message="Kategori başarıyla eklendi.", data=category)


@router.put("/categories/{category_id}")
def update_category(category_id: int, body: CategoryUpdate):
    """Mevcut kategoriyi günceller"""
    category, error = category_service.update_category(
        category_id=category_id,
        name=body.name,
        description=body.description,
        is_active=body.is_active
    )
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Kategori güncellendi.", data=category)


@router.delete("/categories/{category_id}")
def delete_category(category_id: int):
    """Kategoriyi pasife alır"""
    success, error = category_service.delete_category(category_id)
    if error:
        raise HTTPException(status_code=404, detail=error_response(error))
    return success_response(message="Kategori silindi.")
