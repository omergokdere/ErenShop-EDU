"""
product_service.py - Ürün iş mantığı
"""
from app.database import get_connection
from app.utils.helpers import rows_to_list, row_to_dict


def get_all_products():
    """Tüm aktif ürünleri listeler"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE IsActive = 1 ORDER BY CreatedAt DESC")
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def get_product_by_id(product_id: int):
    """ID'ye göre tek ürün getirir"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE Id = ? AND IsActive = 1", product_id)
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    result = row_to_dict(cursor, row)
    conn.close()
    return result


def get_products_by_category(category_id: int):
    """Kategoriye göre ürünleri listeler"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Products WHERE CategoryId = ? AND IsActive = 1 ORDER BY Name",
        category_id
    )
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def search_products(keyword: str):
    """Ürün adı veya açıklamasında anahtar kelime arar"""
    conn = get_connection()
    cursor = conn.cursor()
    # LIKE ile arama - %keyword% → içinde geçen kayıtları bulur
    cursor.execute(
        """
        SELECT * FROM Products
        WHERE IsActive = 1
          AND (Name LIKE ? OR Description LIKE ?)
        ORDER BY Name
        """,
        f"%{keyword}%", f"%{keyword}%"
    )
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def create_product(category_id: int, name: str, description: str, price: float, stock: int):
    """Yeni ürün ekler"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Kategori var mı kontrol et
    cursor.execute("SELECT Id FROM Categories WHERE Id = ? AND IsActive = 1", category_id)
    if not cursor.fetchone():
        conn.close()
        return None, "Belirtilen kategori bulunamadı."
    
    cursor.execute(
        """
        INSERT INTO Products (CategoryId, Name, Description, Price, Stock, IsActive, CreatedAt, UpdatedAt)
        VALUES (?, ?, ?, ?, ?, 1, GETDATE(), GETDATE())
        """,
        category_id, name, description, price, stock
    )
    conn.commit()
    
    cursor.execute("SELECT @@IDENTITY AS Id")
    new_id = int(cursor.fetchone()[0])
    conn.close()
    return get_product_by_id(new_id), None


def update_product(product_id: int, category_id=None, name=None, description=None, price=None, stock=None, is_active=None):
    """Mevcut ürünü günceller"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Products WHERE Id = ?", product_id)
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None, "Ürün bulunamadı."
    
    current = row_to_dict(cursor, row)
    
    new_category_id = category_id if category_id is not None else current["CategoryId"]
    new_name = name if name is not None else current["Name"]
    new_description = description if description is not None else current["Description"]
    new_price = price if price is not None else current["Price"]
    new_stock = stock if stock is not None else current["Stock"]
    new_is_active = is_active if is_active is not None else bool(current["IsActive"])
    
    cursor.execute(
        """
        UPDATE Products
        SET CategoryId = ?, Name = ?, Description = ?, Price = ?, Stock = ?, IsActive = ?, UpdatedAt = GETDATE()
        WHERE Id = ?
        """,
        new_category_id, new_name, new_description, new_price, new_stock,
        1 if new_is_active else 0, product_id
    )
    conn.commit()
    conn.close()
    return get_product_by_id(product_id), None


def delete_product(product_id: int):
    """Ürünü pasife alır"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT Id FROM Products WHERE Id = ? AND IsActive = 1", product_id)
    if not cursor.fetchone():
        conn.close()
        return False, "Ürün bulunamadı."
    
    cursor.execute(
        "UPDATE Products SET IsActive = 0, UpdatedAt = GETDATE() WHERE Id = ?",
        product_id
    )
    conn.commit()
    conn.close()
    return True, None
