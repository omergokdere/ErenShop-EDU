"""
payment_service.py - Mock ödeme iş mantığı
Gerçek ödeme entegrasyonu yoktur.
Eğitim amaçlı başarılı/başarısız simülasyon yapılır.
"""
from app.database import get_connection
from app.utils.helpers import row_to_dict, generate_transaction_code


def process_mock_payment(order_id: int, payment_type: str, amount: float, force_fail: bool = False):
    """
    Mock ödeme işlemi simüle eder.
    
    force_fail=True ise → ödeme başarısız sayılır (hata senaryosu için)
    force_fail=False ise → ödeme başarılı sayılır
    
    Ödeme başarılı olursa:
    - Payments tablosuna kayıt eklenir
    - Orders.Status = 'Paid' yapılır
    
    Ödeme başarısız olursa:
    - Payments tablosuna başarısız kayıt eklenir
    - Orders.Status = 'PaymentFailed' yapılır
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sipariş var mı?
    cursor.execute("SELECT * FROM Orders WHERE Id = ?", order_id)
    order_row = cursor.fetchone()
    if not order_row:
        conn.close()
        return None, "Sipariş bulunamadı."
    
    order = row_to_dict(cursor, order_row)
    
    # Daha önce başarılı ödeme yapılmış mı?
    if order["Status"] == "Paid":
        conn.close()
        return None, "Bu sipariş zaten ödenmiş."
    
    # Benzersiz işlem kodu oluştur
    transaction_code = generate_transaction_code()
    
    # force_fail parametresine göre başarı durumunu belirle
    is_successful = not force_fail
    
    # Ödeme kaydını ekle
    cursor.execute(
        """
        INSERT INTO Payments (OrderId, PaymentType, Amount, IsSuccessful, TransactionCode, CreatedAt)
        VALUES (?, ?, ?, ?, ?, GETDATE())
        """,
        order_id, payment_type, amount, 1 if is_successful else 0, transaction_code
    )
    cursor.execute("SELECT @@IDENTITY AS Id")
    payment_id = int(cursor.fetchone()[0])
    
    # Sipariş durumunu güncelle
    new_status = "Paid" if is_successful else "PaymentFailed"
    cursor.execute(
        "UPDATE Orders SET Status = ?, UpdatedAt = GETDATE() WHERE Id = ?",
        new_status, order_id
    )
    
    conn.commit()
    conn.close()
    
    return {
        "payment_id": payment_id,
        "order_id": order_id,
        "transaction_code": transaction_code,
        "is_successful": is_successful,
        "new_order_status": new_status,
        "amount": amount,
        "payment_type": payment_type
    }, None
