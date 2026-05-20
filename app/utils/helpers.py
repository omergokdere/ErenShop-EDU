"""
helpers.py - Genel yardımcı fonksiyonlar
Projede tekrar kullanılan ortak işlemler burada tanımlanır.
"""
import uuid
from datetime import datetime


def generate_order_number() -> str:
    """
    Benzersiz sipariş numarası üretir.
    Örnek: ORD-20260428-A3F2
    """
    today = datetime.now().strftime("%Y%m%d")
    unique_part = uuid.uuid4().hex[:4].upper()
    return f"ORD-{today}-{unique_part}"


def generate_transaction_code() -> str:
    """
    Ödeme için benzersiz işlem kodu üretir.
    Örnek: TXN-8F3A2B1C
    """
    return f"TXN-{uuid.uuid4().hex[:8].upper()}"


def row_to_dict(cursor, row) -> dict:
    """
    pyodbc satırını Python sözlüğüne dönüştürür.
    cursor.description → sütun isimlerini verir.
    """
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))


def rows_to_list(cursor, rows) -> list:
    """
    pyodbc satır listesini Python sözlük listesine dönüştürür.
    """
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
