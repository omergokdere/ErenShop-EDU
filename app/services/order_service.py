"""
order_service.py - Sipariş iş mantığı
Bu modülde TRANSACTION kullanımı öğretilir.
Transaction: Birden fazla SQL işlemi ya hep birlikte başarılı olur ya da hiçbiri gerçekleşmez.
"""
from app.database import get_connection
from app.utils.helpers import rows_to_list, row_to_dict
from app.utils.helpers import generate_order_number


def create_order_from_cart(customer_id: int):
    """
    Müşterinin sepetini siparişe dönüştürür.
    
    Adımlar:
    1. Müşteri var mı kontrol et
    2. Sepet boş mu kontrol et
    3. Tüm ürünlerin stoğu yeterli mi kontrol et
    4. Transaction başlat
    5. Orders tablosuna kayıt ekle
    6. OrderItems tablosuna satırları ekle
    7. Her ürünün stokunu düş
    8. Sepeti temizle
    9. Transaction'ı commit et
    10. Hata olursa rollback yap
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Müşteri kontrolü
    cursor.execute("SELECT Id FROM Customers WHERE Id = ? AND IsActive = 1", customer_id)
    if not cursor.fetchone():
        conn.close()
        return None, "Müşteri bulunamadı."
    
    # 2. Sepet kontrolü
    cursor.execute(
        "SELECT Id FROM Carts WHERE CustomerId = ? AND IsActive = 1",
        customer_id
    )
    cart_row = cursor.fetchone()
    if not cart_row:
        conn.close()
        return None, "Aktif sepet bulunamadı."
    
    cart_id = cart_row[0]
    
    # Sepet ürünlerini getir
    cursor.execute(
        """
        SELECT ci.Id as CartItemId, ci.ProductId, ci.Quantity, ci.UnitPrice,
               p.Stock, p.Name as ProductName, p.IsActive
        FROM CartItems ci
        INNER JOIN Products p ON ci.ProductId = p.Id
        WHERE ci.CartId = ?
        """,
        cart_id
    )
    cart_items = cursor.fetchall()
    
    if not cart_items:
        conn.close()
        return None, "Sepet boş. Sipariş oluşturulamaz."
    
    # 3. Stok kontrolü - tüm ürünler için
    for item in cart_items:
        cart_item_id, product_id, quantity, unit_price, stock, product_name, is_active = item
        
        if not is_active:
            conn.close()
            return None, f"'{product_name}' ürünü artık aktif değil. Sepetten çıkarın."
        
        if quantity > stock:
            conn.close()
            return None, f"'{product_name}' için yetersiz stok. İstenen: {quantity}, Mevcut: {stock}"
    
    # Toplam tutarı hesapla
    total_amount = sum(item[2] * item[3] for item in cart_items)
    order_number = generate_order_number()
    
    try:
        # 4-8. TRANSACTION - autocommit kapatılmış, değişiklikler commit edilene kadar geçici
        
        # 5. Sipariş oluştur
        cursor.execute(
            """
            INSERT INTO Orders (CustomerId, OrderNumber, TotalAmount, Status, CreatedAt, UpdatedAt)
            VALUES (?, ?, ?, 'Pending', GETDATE(), GETDATE())
            """,
            customer_id, order_number, total_amount
        )
        cursor.execute("SELECT @@IDENTITY AS Id")
        order_id = int(cursor.fetchone()[0])
        
        # 6. Sipariş detaylarını ekle
        for item in cart_items:
            cart_item_id, product_id, quantity, unit_price, stock, product_name, is_active = item
            line_total = quantity * unit_price
            
            cursor.execute(
                """
                INSERT INTO OrderItems (OrderId, ProductId, Quantity, UnitPrice, TotalPrice, CreatedAt)
                VALUES (?, ?, ?, ?, ?, GETDATE())
                """,
                order_id, product_id, quantity, unit_price, line_total
            )
            
            # 7. Stok düş
            cursor.execute(
                "UPDATE Products SET Stock = Stock - ?, UpdatedAt = GETDATE() WHERE Id = ?",
                quantity, product_id
            )
        
        # 8. Sepeti temizle
        cursor.execute("DELETE FROM CartItems WHERE CartId = ?", cart_id)
        
        # 9. Tüm işlemler başarılı → COMMIT
        conn.commit()
        
    except Exception as e:
        # 10. Hata oluştuysa ROLLBACK → Hiçbir değişiklik kaydedilmez
        conn.rollback()
        conn.close()
        return None, f"Sipariş oluşturulurken hata: {str(e)}"
    
    conn.close()
    return get_order_by_id(order_id), None


def get_all_orders():
    """Tüm siparişleri listeler"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders ORDER BY CreatedAt DESC")
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def get_order_by_id(order_id: int):
    """Sipariş ve detaylarını getirir"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sipariş bilgisi
    cursor.execute("SELECT * FROM Orders WHERE Id = ?", order_id)
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    order = row_to_dict(cursor, row)
    
    # Sipariş kalemleri
    cursor.execute(
        """
        SELECT oi.*, p.Name as ProductName
        FROM OrderItems oi
        INNER JOIN Products p ON oi.ProductId = p.Id
        WHERE oi.OrderId = ?
        """,
        order_id
    )
    rows = cursor.fetchall()
    order["items"] = rows_to_list(cursor, rows)
    
    conn.close()
    return order


def get_order_by_number(order_number: str):
    """Sipariş numarasına göre sipariş ve detaylarını getirir"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Orders WHERE OrderNumber = ?", order_number)
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    order = row_to_dict(cursor, row)

    cursor.execute(
        """
        SELECT oi.*, p.Name as ProductName
        FROM OrderItems oi
        INNER JOIN Products p ON oi.ProductId = p.Id
        WHERE oi.OrderId = ?
        """,
        order["Id"]
    )
    rows = cursor.fetchall()
    order["items"] = rows_to_list(cursor, rows)

    conn.close()
    return order


def get_orders_by_customer(customer_id: int):
    """Müşteriye ait siparişleri getirir"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Orders WHERE CustomerId = ? ORDER BY CreatedAt DESC",
        customer_id
    )
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def update_order_status(order_id: int, status: str):
    """Sipariş durumunu günceller"""
    # Geçerli durumlar
    valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled", "Paid", "PaymentFailed"]
    if status not in valid_statuses:
        return None, f"Geçersiz durum. Geçerli değerler: {', '.join(valid_statuses)}"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT Id FROM Orders WHERE Id = ?", order_id)
    if not cursor.fetchone():
        conn.close()
        return None, "Sipariş bulunamadı."
    
    cursor.execute(
        "UPDATE Orders SET Status = ?, UpdatedAt = GETDATE() WHERE Id = ?",
        status, order_id
    )
    conn.commit()
    conn.close()
    return get_order_by_id(order_id), None
