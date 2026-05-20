"""
report_service.py - Raporlama iş mantığı
GROUP BY, SUM, COUNT, JOIN kullanımı öğretilir.
"""
from app.database import get_connection
from app.utils.helpers import rows_to_list


def get_daily_sales(date_str: str = None):
    """
    Günlük satış raporu.
    date_str verilmezse bugünün verilerini getirir.
    Öğretici nokta: CAST ile tarih karşılaştırma, SUM ile toplama.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if date_str:
        cursor.execute(
            """
            SELECT
                CAST(o.CreatedAt AS DATE) as SaleDate,
                COUNT(DISTINCT o.Id) as OrderCount,
                SUM(o.TotalAmount) as TotalRevenue
            FROM Orders o
            WHERE o.Status = 'Paid'
              AND CAST(o.CreatedAt AS DATE) = ?
            GROUP BY CAST(o.CreatedAt AS DATE)
            """,
            date_str
        )
    else:
        # Bugünün tarihi
        cursor.execute(
            """
            SELECT
                CAST(o.CreatedAt AS DATE) as SaleDate,
                COUNT(DISTINCT o.Id) as OrderCount,
                SUM(o.TotalAmount) as TotalRevenue
            FROM Orders o
            WHERE o.Status = 'Paid'
              AND CAST(o.CreatedAt AS DATE) = CAST(GETDATE() AS DATE)
            GROUP BY CAST(o.CreatedAt AS DATE)
            """
        )
    
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def get_top_products(limit: int = 10):
    """
    En çok satılan ürünler.
    Öğretici nokta: JOIN + GROUP BY + ORDER BY + TOP.
    """
    # limit değerini integer olarak kontrol et (güvenlik)
    limit = max(1, min(int(limit), 100))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        f"""
        SELECT TOP {limit}
            p.Id as ProductId,
            p.Name as ProductName,
            c.Name as CategoryName,
            SUM(oi.Quantity) as TotalSold,
            SUM(oi.TotalPrice) as TotalRevenue
        FROM OrderItems oi
        INNER JOIN Products p ON oi.ProductId = p.Id
        INNER JOIN Categories c ON p.CategoryId = c.Id
        INNER JOIN Orders o ON oi.OrderId = o.Id
        WHERE o.Status = 'Paid'
        GROUP BY p.Id, p.Name, c.Name
        ORDER BY TotalSold DESC
        """
    )
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def get_customer_summary(customer_id: int):
    """
    Müşteri bazlı sipariş özeti.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT
            cu.Id as CustomerId,
            cu.FirstName + ' ' + cu.LastName as CustomerName,
            cu.Email,
            COUNT(DISTINCT o.Id) as TotalOrders,
            SUM(CASE WHEN o.Status = 'Paid' THEN o.TotalAmount ELSE 0 END) as TotalSpent,
            MAX(o.CreatedAt) as LastOrderDate
        FROM Customers cu
        LEFT JOIN Orders o ON cu.Id = o.CustomerId
        WHERE cu.Id = ?
        GROUP BY cu.Id, cu.FirstName, cu.LastName, cu.Email
        """,
        customer_id
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    columns = [col[0] for col in cursor.description]
    result = dict(zip(columns, row))
    conn.close()
    return result


def get_category_sales():
    """
    Kategori bazlı satış özeti.
    Öğretici nokta: Çoklu JOIN + GROUP BY.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT
            c.Id as CategoryId,
            c.Name as CategoryName,
            COUNT(DISTINCT o.Id) as OrderCount,
            SUM(oi.Quantity) as TotalItemsSold,
            SUM(oi.TotalPrice) as TotalRevenue
        FROM Categories c
        LEFT JOIN Products p ON c.Id = p.CategoryId
        LEFT JOIN OrderItems oi ON p.Id = oi.ProductId
        LEFT JOIN Orders o ON oi.OrderId = o.Id AND o.Status = 'Paid'
        WHERE c.IsActive = 1
        GROUP BY c.Id, c.Name
        ORDER BY TotalRevenue DESC
        """
    )
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result


def get_low_stock_products(threshold: int = 10):
    """
    Stoğu azalan ürünler.
    Öğretici nokta: WHERE ile eşik değeri filtresi.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT p.Id, p.Name, c.Name as CategoryName, p.Stock, p.Price
        FROM Products p
        INNER JOIN Categories c ON p.CategoryId = c.Id
        WHERE p.IsActive = 1 AND p.Stock <= ?
        ORDER BY p.Stock ASC
        """,
        threshold
    )
    rows = cursor.fetchall()
    result = rows_to_list(cursor, rows)
    conn.close()
    return result
