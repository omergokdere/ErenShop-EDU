-- ============================================================
-- 04_training_select_queries.sql
-- TEMEL SELECT SORGULARI - Eğitim Notları
-- Bu sorguları SSMS'te tek tek çalıştırarak öğren.
-- ============================================================

USE ErenShopDB;
GO

-- ============================================================
-- DERS 1: Tüm verileri getir (SELECT *)
-- ============================================================

-- Tüm kategorileri getir
SELECT * FROM Categories;

-- Tüm ürünleri getir
SELECT * FROM Products;

-- Tüm müşterileri getir
SELECT * FROM Customers;


-- ============================================================
-- DERS 2: Belirli sütunları seç
-- ============================================================

-- Sadece ürün adı ve fiyatını göster
SELECT Name, Price FROM Products;

-- Müşteri adı ve emailini göster
SELECT FirstName, LastName, Email FROM Customers;


-- ============================================================
-- DERS 3: WHERE ile filtreleme
-- ============================================================

-- Sadece aktif ürünleri listele
SELECT * FROM Products WHERE IsActive = 1;

-- Stok miktarı 10'dan az olan ürünler (kritik stok)
SELECT Id, Name, Stock FROM Products WHERE Stock < 10;

-- Fiyatı 500'den büyük ürünler
SELECT Name, Price FROM Products WHERE Price > 500;

-- Belirli bir kategorideki ürünler (CategoryId = 1 = Elektronik)
SELECT Name, Price, Stock FROM Products WHERE CategoryId = 1 AND IsActive = 1;


-- ============================================================
-- DERS 4: LIKE ile arama
-- ============================================================

-- Adında "Mouse" geçen ürünler
-- % → sıfır veya daha fazla herhangi bir karakter
SELECT * FROM Products WHERE Name LIKE '%Mouse%';

-- Adı "Kab" ile başlayan ürünler
SELECT * FROM Products WHERE Name LIKE 'Kab%';

-- Açıklamasında "LED" geçen ürünler
SELECT * FROM Products WHERE Description LIKE '%LED%';


-- ============================================================
-- DERS 5: ORDER BY ile sıralama
-- ============================================================

-- Ürünleri fiyata göre artan sırala (ucuzdan pahalıya)
SELECT Name, Price FROM Products ORDER BY Price ASC;

-- Ürünleri fiyata göre azalan sırala (pahalıdan ucuza)
SELECT Name, Price FROM Products ORDER BY Price DESC;

-- Müşterileri soyadına göre alfabetik sırala
SELECT FirstName, LastName FROM Customers ORDER BY LastName ASC;


-- ============================================================
-- DERS 6: TOP ile sınırlama
-- ============================================================

-- En pahalı 5 ürünü getir
SELECT TOP 5 Name, Price FROM Products ORDER BY Price DESC;

-- En son eklenen 3 müşteri
SELECT TOP 3 FirstName, LastName, CreatedAt
FROM Customers
ORDER BY CreatedAt DESC;


-- ============================================================
-- DERS 7: BETWEEN ile aralık filtresi
-- ============================================================

-- Fiyatı 100 ile 500 arasındaki ürünler
SELECT Name, Price FROM Products WHERE Price BETWEEN 100 AND 500;

-- Stok miktarı 10 ile 30 arasındaki ürünler
SELECT Name, Stock FROM Products WHERE Stock BETWEEN 10 AND 30;


-- ============================================================
-- DERS 8: IN ile çoklu değer filtresi
-- ============================================================

-- CategoryId 1 veya 2 olan ürünler
SELECT Name, CategoryId FROM Products WHERE CategoryId IN (1, 2);

-- Durumu 'Pending' veya 'Paid' olan siparişler
SELECT * FROM Orders WHERE Status IN ('Pending', 'Paid');


-- ============================================================
-- DERS 9: NULL kontrolü
-- ============================================================

-- Telefon numarası girilmemiş müşteriler
SELECT FirstName, LastName, Email FROM Customers WHERE Phone IS NULL;

-- Açıklaması olan ürünler
SELECT Name FROM Products WHERE Description IS NOT NULL;


-- ============================================================
-- DERS 10: Alias (takma ad) kullanımı
-- ============================================================

-- Sütun isimlerini Türkçe göster
SELECT
    Name        AS 'Ürün Adı',
    Price       AS 'Fiyat',
    Stock       AS 'Stok Miktarı'
FROM Products
WHERE IsActive = 1
ORDER BY Price DESC;
