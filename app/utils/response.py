"""
response.py - Standart API cevap formatı
Tüm endpoint'ler bu yardımcı fonksiyonları kullanır.
Böylece her cevap aynı formatta döner.
"""
from typing import Any, Optional


def success_response(message: str = "İşlem başarılı.", data: Any = None) -> dict:
    """
    Başarılı işlemlerde kullanılan standart cevap formatı.
    
    Örnek:
    {
        "success": true,
        "message": "Kategori başarıyla eklendi.",
        "data": { "id": 1, "name": "Elektronik" }
    }
    """
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str = "Bir hata oluştu.", data: Any = None) -> dict:
    """
    Hatalı işlemlerde kullanılan standart cevap formatı.
    
    Örnek:
    {
        "success": false,
        "message": "Kategori bulunamadı.",
        "data": null
    }
    """
    return {
        "success": False,
        "message": message,
        "data": data
    }
