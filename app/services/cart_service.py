"""
cart_service.py - Sepet iş mantığı
"""
from app.database import get_connection
from app.utils.helpers import rows_to_list, row_to_dict


def _get_or_create_cart(cursor, customer_id: int) -> int:
    """
    Müşterinin aktif sepetini getirir.
    Yoksa yeni sepet oluşturur.
    Bu fonksiyon sadece bu modül içinde kullanılır (private).
    """
    cursor.execute(
        "SELECT Id FROM Carts WHERE CustomerId = ? AND IsActive = 1",
        customer_id
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    
    # Sepet yok, oluştur
    cursor.execute(
        "INSERT INTO Carts (CustomerId, IsActive, CreatedAt, UpdatedAt) VALUES (?, 1, GETDATE(), GETDATE())",
        customer_id
    )
    cursor.execute("SELECT @@IDENTITY AS Id")
    return int(cursor.fetchone()[0])


def add_to_cart(customer_id: int, product_id: int, quantity: int):
    """Sepete ürün ekler"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Müşteri var mı?
    cursor.execute("SELECT Id FROM Customers WHERE Id = ? AND IsActive = 1", customer_id)
    if not cursor.fetchone():
        conn.close()
        return None, "Müşteri bulunamadı."
    
    # Ürün aktif mi ve stok yeterli mi?
    cursor.execute("SELECT Id, Stock, Price, IsActive FROM Products WHERE Id = ?", product_id)
    product_row = cursor.fetchone()
    if not product_row or not product_row[3]:
        conn.close()
        return None, "Ürün bulunamadı veya aktif değil."
    
    product_stock = product_row[1]
    product_price = product_row[2]
    
    # Sepeti al veya oluştur
    cart_id = _get_or_create_cart(cursor, customer_id)
    
    # Ürün zaten sepette var mı?
    cursor.execute(
        "SELECT Id, Quantity FROM CartItems WHERE CartId = ? AND ProductId = ?",
        cart_id, product_id
    )
    existing_item = cursor.fetchone()
    
    if existing_item:
        # Varsa miktarı güncelle
        new_quantity = existing_item[1] + quantity
        if new_quantity > product_stock:
            conn.close()
            return None, f"Yetersiz stok. Mevcut stok: {product_stock}"
        cursor.execute(
            "UPDATE CartItems SET Quantity = ?, UpdatedAt = GETDATE() WHERE Id = ?",
            new_quantity, existing_item[0]
        )
    else:
        # Yoksa yeni satır ekle
        if quantity > product_stock:
            conn.close()
            return None, f"Yetersiz stok. Mevcut stok: {product_stock}"
        cursor.execute(
            """
            INSERT INTO CartItems (CartId, ProductId, Quantity, UnitPrice, CreatedAt, UpdatedAt)
            VALUES (?, ?, ?, ?, GETDATE(), GETDATE())
            """,
            cart_id, product_id, quantity, product_price
        )
    
    conn.commit()
    conn.close()
    return get_cart(customer_id), None


def get_cart(customer_id: int):
    """Müşterinin sepetini ve ürünlerini getirir"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sepet bilgisi
    cursor.execute(
        "SELECT Id FROM Carts WHERE CustomerId = ? AND IsActive = 1",
        customer_id
    )
    cart_row = cursor.fetchone()
    if not cart_row:
        conn.close()
        return {"cart_id": None, "items": [], "total": 0}
    
    cart_id = cart_row[0]
    
    # Sepet ürünlerini ürün adıyla birlikte getir (JOIN)
    cursor.execute(
        """
        SELECT ci.Id as CartItemId, p.Id as ProductId, p.Name as ProductName,
               ci.Quantity, ci.UnitPrice, (ci.Quantity * ci.UnitPrice) as LineTotal
        FROM CartItems ci
        INNER JOIN Products p ON ci.ProductId = p.Id
        WHERE ci.CartId = ?
        ORDER BY ci.CreatedAt
        """,
        cart_id
    )
    rows = cursor.fetchall()
    items = rows_to_list(cursor, rows)
    
    # Toplam tutarı hesapla
    total = sum(item["LineTotal"] for item in items)
    
    conn.close()
    return {
        "cart_id": cart_id,
        "customer_id": customer_id,
        "items": items,
        "total": round(total, 2)
    }


def remove_cart_item(cart_item_id: int):
    """Sepetten tek bir ürünü siler"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT Id FROM CartItems WHERE Id = ?", cart_item_id)
    if not cursor.fetchone():
        conn.close()
        return False, "Sepet ürünü bulunamadı."
    
    cursor.execute("DELETE FROM CartItems WHERE Id = ?", cart_item_id)
    conn.commit()
    conn.close()
    return True, None


def clear_cart(customer_id: int):
    """Müşterinin sepetini tamamen temizler"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Aktif sepeti bul
    cursor.execute(
        "SELECT Id FROM Carts WHERE CustomerId = ? AND IsActive = 1",
        customer_id
    )
    cart_row = cursor.fetchone()
    if not cart_row:
        conn.close()
        return False, "Aktif sepet bulunamadı."
    
    cart_id = cart_row[0]
    cursor.execute("DELETE FROM CartItems WHERE CartId = ?", cart_id)
    conn.commit()
    conn.close()
    return True, None
