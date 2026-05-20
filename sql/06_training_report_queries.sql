-- ============================================================
-- 06_training_report_queries.sql
-- RAPORLAMA SORGULARI - GROUP BY, SUM, COUNT, AVG
-- ============================================================

USE ErenShopDB;
GO

-- ============================================================
-- DERS 1: COUNT - Kayıt sayma
-- ============================================================

-- Toplam kaç müşteri var?
SELECT COUNT(*) AS TotalCustomers FROM Customers WHERE IsActive = 1;

-- Toplam kaç ürün var?
SELECT COUNT(*) AS TotalProducts FROM Products WHERE IsActive = 1;

-- Toplam kaç sipariş var?
SELECT COUNT(*) AS TotalOrders FROM Orders;

-- Duruma göre sipariş sayısı (GROUP BY öğretici örnek)
SELECT
    Status,
    COUNT(*) AS OrderCount
FROM Orders
GROUP BY Status
ORDER BY OrderCount DESC;


-- ============================================================
-- DERS 2: SUM - Toplam hesaplama
-- ============================================================

-- Tüm ödenmiş siparişlerin toplam tutarı
SELECT SUM(TotalAmount) AS TotalRevenue
FROM Orders
WHERE Status = 'Paid';

-- Kategori bazında toplam stok değeri
SELECT
    c.Name AS CategoryName,
    SUM(p.Stock * p.Price) AS StockValue   -- Stok adet x fiyat = değer
FROM Products p
INNER JOIN Categories c ON p.CategoryId = c.Id
WHERE p.IsActive = 1
GROUP BY c.Id, c.Name
ORDER BY StockValue DESC;


-- ============================================================
-- DERS 3: AVG - Ortalama hesaplama
-- ============================================================

-- Ortalama ürün fiyatı
SELECT AVG(Price) AS AveragePrice FROM Products WHERE IsActive = 1;

-- Kategori bazında ortalama ürün fiyatı
SELECT
    c.Name AS CategoryName,
    AVG(p.Price) AS AveragePrice,
    MIN(p.Price) AS MinPrice,
    MAX(p.Price) AS MaxPrice
FROM Products p
INNER JOIN Categories c ON p.CategoryId = c.Id
WHERE p.IsActive = 1
GROUP BY c.Id, c.Name
ORDER BY AveragePrice DESC;


-- ============================================================
-- DERS 4: Günlük satış raporu
-- ============================================================
SELECT
    CAST(o.CreatedAt AS DATE)   AS SaleDate,
    COUNT(DISTINCT o.Id)        AS OrderCount,
    SUM(o.TotalAmount)          AS TotalRevenue
FROM Orders o
WHERE o.Status = 'Paid'
GROUP BY CAST(o.CreatedAt AS DATE)
ORDER BY SaleDate DESC;


-- ============================================================
-- DERS 5: En çok satılan ürünler
-- ============================================================
SELECT TOP 10
    p.Name          AS ProductName,
    c.Name          AS CategoryName,
    SUM(oi.Quantity)    AS TotalSold,
    SUM(oi.TotalPrice)  AS TotalRevenue
FROM OrderItems oi
INNER JOIN Products p   ON oi.ProductId = p.Id
INNER JOIN Categories c ON p.CategoryId = c.Id
INNER JOIN Orders o     ON oi.OrderId   = o.Id
WHERE o.Status = 'Paid'
GROUP BY p.Id, p.Name, c.Name
ORDER BY TotalSold DESC;


-- ============================================================
-- DERS 6: Müşteri bazlı toplam harcama
-- ============================================================
SELECT
    cu.FirstName + ' ' + cu.LastName AS CustomerName,
    cu.Email,
    COUNT(DISTINCT o.Id)    AS TotalOrders,
    SUM(o.TotalAmount)      AS TotalSpent
FROM Customers cu
INNER JOIN Orders o ON cu.Id = o.CustomerId
WHERE o.Status = 'Paid'
GROUP BY cu.Id, cu.FirstName, cu.LastName, cu.Email
ORDER BY TotalSpent DESC;


-- ============================================================
-- DERS 7: Kategori bazlı satış raporu
-- ============================================================
SELECT
    c.Name          AS CategoryName,
    COUNT(DISTINCT o.Id)        AS OrderCount,
    SUM(oi.Quantity)            AS TotalItemsSold,
    SUM(oi.TotalPrice)          AS TotalRevenue
FROM Categories c
INNER JOIN Products p   ON c.Id         = p.CategoryId
INNER JOIN OrderItems oi ON p.Id        = oi.ProductId
INNER JOIN Orders o      ON oi.OrderId  = o.Id
WHERE o.Status = 'Paid' AND c.IsActive = 1
GROUP BY c.Id, c.Name
ORDER BY TotalRevenue DESC;


-- ============================================================
-- DERS 8: Stok azalan ürünler (eşik = 10)
-- ============================================================
SELECT
    p.Name          AS ProductName,
    c.Name          AS CategoryName,
    p.Stock,
    p.Price,
    CASE
        WHEN p.Stock = 0 THEN 'Tükendi!'
        WHEN p.Stock <= 5 THEN 'Kritik Stok'
        ELSE 'Düşük Stok'
    END AS StockStatus   -- CASE WHEN ile koşullu etiket
FROM Products p
INNER JOIN Categories c ON p.CategoryId = c.Id
WHERE p.IsActive = 1 AND p.Stock <= 10
ORDER BY p.Stock ASC;


-- ============================================================
-- DERS 9: HAVING - Gruplandırılmış veriyi filtreleme
-- (WHERE gruplama öncesi, HAVING gruplama sonrası filtreler)
-- ============================================================

-- En az 2 ürünü olan kategoriler
SELECT
    c.Name AS CategoryName,
    COUNT(p.Id) AS ProductCount
FROM Categories c
INNER JOIN Products p ON c.Id = p.CategoryId
WHERE p.IsActive = 1
GROUP BY c.Id, c.Name
HAVING COUNT(p.Id) >= 2   -- Gruplama sonrası filtre: 2 veya daha fazla ürünü olanlar
ORDER BY ProductCount DESC;
