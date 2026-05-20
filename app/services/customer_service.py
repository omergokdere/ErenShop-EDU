"""
customer_service.py - Müşteri iş mantığı
"""
from app.database import get_connection
from app.utils.helpers import rows_to_list, row_to_dict


def get_all_customers():
    """Tüm aktif müşterileri listeler"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers WHERE IsActive = 1 ORDER BY CreatedAt DESC")
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def get_customer_by_id(customer_id: int):
    """ID'ye göre tek müşteri getirir"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers WHERE Id = ? AND IsActive = 1", customer_id)
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    result = row_to_dict(cursor, row)
    conn.close()
    return result


def create_customer(first_name: str, last_name: str, email: str, phone: str = None, address: str = None):
    """Yeni müşteri ekler"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Email benzersiz olmalı
    cursor.execute("SELECT Id FROM Customers WHERE Email = ? AND IsActive = 1", email)
    if cursor.fetchone():
        conn.close()
        return None, "Bu e-posta adresi zaten kayıtlı."
    
    cursor.execute(
        """
        INSERT INTO Customers (FirstName, LastName, Email, Phone, Address, IsActive, CreatedAt, UpdatedAt)
        VALUES (?, ?, ?, ?, ?, 1, GETDATE(), GETDATE())
        """,
        first_name, last_name, email, phone, address
    )
    conn.commit()
    
    cursor.execute("SELECT @@IDENTITY AS Id")
    new_id = int(cursor.fetchone()[0])
    conn.close()
    return get_customer_by_id(new_id), None


def update_customer(customer_id: int, first_name=None, last_name=None, email=None, phone=None, address=None, is_active=None):
    """Müşteri bilgilerini günceller"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Customers WHERE Id = ?", customer_id)
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None, "Müşteri bulunamadı."
    
    current = row_to_dict(cursor, row)
    
    new_first_name = first_name if first_name is not None else current["FirstName"]
    new_last_name = last_name if last_name is not None else current["LastName"]
    new_email = email if email is not None else current["Email"]
    new_phone = phone if phone is not None else current["Phone"]
    new_address = address if address is not None else current["Address"]
    new_is_active = is_active if is_active is not None else bool(current["IsActive"])
    
    cursor.execute(
        """
        UPDATE Customers
        SET FirstName = ?, LastName = ?, Email = ?, Phone = ?, Address = ?, IsActive = ?, UpdatedAt = GETDATE()
        WHERE Id = ?
        """,
        new_first_name, new_last_name, new_email, new_phone, new_address,
        1 if new_is_active else 0, customer_id
    )
    conn.commit()
    conn.close()
    return get_customer_by_id(customer_id), None


def delete_customer(customer_id: int):
    """Müşteriyi pasife alır"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT Id FROM Customers WHERE Id = ? AND IsActive = 1", customer_id)
    if not cursor.fetchone():
        conn.close()
        return False, "Müşteri bulunamadı."
    
    cursor.execute(
        "UPDATE Customers SET IsActive = 0, UpdatedAt = GETDATE() WHERE Id = ?",
        customer_id
    )
    conn.commit()
    conn.close()
    return True, None


def get_customer_orders(customer_id: int):
    """Müşteriye ait tüm siparişleri getirir"""
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
