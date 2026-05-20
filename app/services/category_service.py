"""
category_service.py - Kategori iş mantığı
Veritabanı işlemleri burada yapılır.
"""
from app.database import get_connection
from app.utils.helpers import rows_to_list, row_to_dict


def get_all_categories():
    """Tüm aktif kategorileri listeler"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sadece aktif kategorileri getir
    cursor.execute("SELECT * FROM Categories WHERE IsActive = 1 ORDER BY CreatedAt DESC")
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    
    conn.close()
    return result


def get_category_by_id(category_id: int):
    """ID'ye göre tek kategori getirir"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Categories WHERE Id = ? AND IsActive = 1", category_id)
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    result = row_to_dict(cursor, row)
    conn.close()
    return result


def create_category(name: str, description: str):
    """Yeni kategori ekler"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Aynı isimde kategori var mı kontrol et
    cursor.execute("SELECT Id FROM Categories WHERE Name = ? AND IsActive = 1", name)
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return None, "Bu isimde bir kategori zaten mevcut."
    
    # Yeni kategoriyi ekle
    cursor.execute(
        """
        INSERT INTO Categories (Name, Description, IsActive, CreatedAt, UpdatedAt)
        VALUES (?, ?, 1, GETDATE(), GETDATE())
        """,
        name, description
    )
    conn.commit()
    
    # Eklenen kaydın ID'sini al
    cursor.execute("SELECT @@IDENTITY AS Id")
    new_id = cursor.fetchone()[0]
    
    conn.close()
    return get_category_by_id(int(new_id)), None


def update_category(category_id: int, name: str = None, description: str = None, is_active: bool = None):
    """Mevcut kategoriyi günceller"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Kategori var mı kontrol et
    cursor.execute("SELECT * FROM Categories WHERE Id = ?", category_id)
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None, "Kategori bulunamadı."
    
    # Mevcut değerleri al
    current = row_to_dict(cursor, row)
    
    # Gelen değerleri veya mevcut değerleri kullan
    new_name = name if name is not None else current["Name"]
    new_description = description if description is not None else current["Description"]
    new_is_active = is_active if is_active is not None else bool(current["IsActive"])
    
    cursor.execute(
        """
        UPDATE Categories
        SET Name = ?, Description = ?, IsActive = ?, UpdatedAt = GETDATE()
        WHERE Id = ?
        """,
        new_name, new_description, 1 if new_is_active else 0, category_id
    )
    conn.commit()
    conn.close()
    
    return get_category_by_id(category_id), None


def delete_category(category_id: int):
    """Kategoriyi pasife alır (soft delete)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Kategori var mı kontrol et
    cursor.execute("SELECT Id FROM Categories WHERE Id = ? AND IsActive = 1", category_id)
    if not cursor.fetchone():
        conn.close()
        return False, "Kategori bulunamadı."
    
    # Soft delete: IsActive = 0
    cursor.execute(
        "UPDATE Categories SET IsActive = 0, UpdatedAt = GETDATE() WHERE Id = ?",
        category_id
    )
    conn.commit()
    conn.close()
    return True, None
