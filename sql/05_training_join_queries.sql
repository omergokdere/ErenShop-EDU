-- ============================================================
-- 05_training_join_queries.sql
-- JOIN SORGULARI - Eğitim Notları
-- JOIN: İki veya daha fazla tabloyu birleştirerek sorgulama yapar.
-- ============================================================

USE ErenShopDB;
GO

-- ============================================================
-- DERS 1: INNER JOIN - Temel kullanım
-- Sadece her iki tabloda da eşleşen kayıtları getirir.
-- ============================================================

-- Ürünleri kategori adıyla birlikte listele
-- Mantık: Products.CategoryId = Categories.Id
SELECT
    p.Id            AS ProductId,
    p.Name          AS ProductName,
    p.Price,
    p.Stock,
    c.Name          AS CategoryName   -- Kategori adı Categories tablosundan geliyor
FROM Products p
INNER JOIN Categories c ON p.CategoryId = c.Id
WHERE p.IsActive = 1
ORDER BY c.Name, p.Name;


-- ============================================================
-- DERS 2: Siparişleri müşteri adıyla listele
-- Orders ← Customers JOIN
-- ============================================================
SELECT
    o.Id            AS OrderId,
    o.OrderNumber,
    o.TotalAmount,
    o.Status,
    o.CreatedAt,
    cu.FirstName + ' ' + cu.LastName AS CustomerName,  -- Ad ve soyadı birleştir
    cu.Email
FROM Orders o
INNER JOIN Customers cu ON o.CustomerId = cu.Id
ORDER BY o.CreatedAt DESC;


-- ============================================================
-- DERS 3: Sipariş detaylarını ürün adıyla listele
-- OrderItems ← Products JOIN
-- ============================================================
SELECT
    oi.Id           AS OrderItemId,
    oi.OrderId,
    p.Name          AS ProductName,
    oi.Quantity,
    oi.UnitPrice,
    oi.TotalPrice
FROM OrderItems oi
INNER JOIN Products p ON oi.ProductId = p.Id
ORDER BY oi.OrderId;


-- ============================================================
-- DERS 4: Üç tabloyu birden join et
-- Siparişleri hem müşteri hem ürün bilgisiyle getir
-- Orders ← Customers + OrderItems ← Products
-- ============================================================
SELECT
    o.OrderNumber,
    cu.FirstName + ' ' + cu.LastName AS CustomerName,
    p.Name          AS ProductName,
    oi.Quantity,
    oi.UnitPrice,
    oi.TotalPrice,
    o.Status
FROM Orders o
INNER JOIN Customers cu    ON o.CustomerId  = cu.Id
INNER JOIN OrderItems oi   ON o.Id          = oi.OrderId
INNER JOIN Products p      ON oi.ProductId  = p.Id
ORDER BY o.CreatedAt DESC;


-- ============================================================
-- DERS 5: Belirli bir müşterinin tüm siparişleri
-- (Müşteri Id = 1 için örnek)
-- ============================================================
SELECT
    o.OrderNumber,
    o.TotalAmount,
    o.Status,
    o.CreatedAt,
    p.Name AS ProductName,
    oi.Quantity,
    oi.TotalPrice
FROM Orders o
INNER JOIN OrderItems oi ON o.Id = oi.OrderId
INNER JOIN Products p    ON oi.ProductId = p.Id
WHERE o.CustomerId = 1
ORDER BY o.CreatedAt DESC;


-- ============================================================
-- DERS 6: LEFT JOIN - Eşleşme olmasa bile sol tabloyu getir
-- Tüm müşterileri, hiç siparişi olmayanlar dahil listele
-- ============================================================
SELECT
    cu.FirstName + ' ' + cu.LastName AS CustomerName,
    cu.Email,
    COUNT(o.Id)     AS TotalOrders,     -- Sipariş yoksa 0 döner
    SUM(ISNULL(o.TotalAmount, 0)) AS TotalSpent   -- NULL varsa 0 kullan
FROM Customers cu
LEFT JOIN Orders o ON cu.Id = o.CustomerId
WHERE cu.IsActive = 1
GROUP BY cu.Id, cu.FirstName, cu.LastName, cu.Email
ORDER BY TotalOrders DESC;


-- ============================================================
-- DERS 7: Sepet içeriklerini müşteri ve ürün bilgisiyle getir
-- ============================================================
SELECT
    cu.FirstName + ' ' + cu.LastName AS CustomerName,
    p.Name          AS ProductName,
    ci.Quantity,
    ci.UnitPrice,
    (ci.Quantity * ci.UnitPrice) AS LineTotal
FROM Carts ca
INNER JOIN Customers cu  ON ca.CustomerId = cu.Id
INNER JOIN CartItems ci  ON ca.Id = ci.CartId
INNER JOIN Products p    ON ci.ProductId  = p.Id
WHERE ca.IsActive = 1
ORDER BY cu.LastName;
