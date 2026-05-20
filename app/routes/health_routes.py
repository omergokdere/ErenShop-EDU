"""
health_routes.py - Sağlık kontrolü endpoint'leri
API'nin çalışıp çalışmadığını ve veritabanı bağlantısını kontrol eder.
"""
from fastapi import APIRouter
from app.database import get_connection
from app.utils.response import success_response, error_response

router = APIRouter()


@router.get("/health")
def health_check():
    """API ve veritabanı sağlık kontrolü"""
    try:
        # Veritabanına bağlanmayı dene
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # En basit sorgu
        conn.close()
        
        return success_response(
            message="API ve veritabanı bağlantısı sağlıklı.",
            data={
                "api": "ok",
                "database": "ok"
            }
        )
    except Exception as e:
        return error_response(
            message=f"Veritabanı bağlantı hatası: {str(e)}",
        )
